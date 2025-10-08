import os
from typing import Literal

from langchain_openai import ChatOpenAI
from openai import OpenAI
from langgraph.graph import StateGraph, START
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import MessagesState, END
from langgraph.types import Command
from langgraph.prebuilt import create_react_agent
from tools import tavily_tool, duckduckgo_tool, python_repl_tool, print_pretty
from prompts import make_system_prompt, chart_task

TOKEN = os.environ["GITHUB_TOKEN"]
ENDPOINT = "https://models.github.ai/inference"
MODEL = "openai/gpt-5-mini"

## Defino o meu llm
llm = ChatOpenAI(
    model=MODEL,
    base_url=ENDPOINT,
    api_key=TOKEN,
)

## Agentes
research_agent = create_react_agent(
    llm,
    tools=[duckduckgo_tool],
    # tools=[tavily_tool],
    prompt=make_system_prompt(
        "Você é um agente que realiza apenas pesquisa. Você está trabalhando com um colega que gera gráficos."
    ),
)

# Chart generator agent
# NOTE: THIS PERFORMS ARBITRARY CODE EXECUTION, WHICH CAN BE UNSAFE WHEN NOT SANDBOXED
chart_agent = create_react_agent(
    llm,
    [python_repl_tool],
    prompt=make_system_prompt(chart_task),
)


## State Graph Nodes
def research_node(
    state: MessagesState,
) -> Command[Literal["chart_generator", END]]:
    result = research_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "chart_generator")
    # wrap in a human message, as not all providers allow
    # AI message at the last position of the input messages list
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="researcher"
    )
    return Command(
        update={
            # share internal message history of research agent with other agents
            "messages": result["messages"],
        },
        goto=goto,
    )


def chart_node(state: MessagesState) -> Command[Literal["researcher", END]]:
    result = chart_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "researcher")
    # wrap in a human message, as not all providers allow
    # AI message at the last position of the input messages list
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="chart_generator"
    )
    return Command(
        update={
            # share internal message history of chart agent with other agents
            "messages": result["messages"],
        },
        goto=goto,
    )


def tool_node(state):
    """This runs tools in the graph It takes in an agent action and calls that tool and returns the result."""
    messages = state["messages"]
    # Based on the continue condition
    # we know the last message involves a function call
    last_message = messages[-1]
    # We construct an ToolInvocation from the function_call
    tool_input = json.loads(
        last_message.additional_kwargs["function_call"]["arguments"]
    )
    # We can pass single-arg inputs by value
    if len(tool_input) == 1 and "__arg1" in tool_input:
        tool_input = next(iter(tool_input.values()))
    tool_name = last_message.additional_kwargs["function_call"]["name"]
    action = ToolInvocation(
        tool=tool_name,
        tool_input=tool_input,
    )
    # We call the tool_executor and get back a response
    response = tool_executor.invoke(action)
    # We use the response to create a FunctionMessage
    function_message = FunctionMessage(
        content=f"{tool_name} response: {str(response)}", name=action.tool
    )
    # We return a list, because this will get added to the existing list
    # return {"messages": [function_message]}
    return Command(
        update={
            "messages": [function_message],
        },
        goto=goto,
    )


# Either agent can decide to end
def router(state):
    # This is the router
    messages = state["messages"]
    last_message = messages[-1]
    if "function_call" in last_message.additional_kwargs:
        # The previus agent is invoking a tool
        return "call_tool"
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return "end"
    return "continue"


def get_next_node(last_message: BaseMessage, goto: str):
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return END
    return goto


def get_graph():
    workflow = StateGraph(MessagesState)
    # nodes
    workflow.add_node("researcher", research_node)
    workflow.add_node("chart_generator", chart_node)
    workflow.add_node("call_tool", tool_node)
    # edges
    workflow.add_edge(START, "researcher")
    workflow.add_conditional_edges(
        "chart_generator",
        router,
        {"continue": "researcher", "call_tool": "call_tool", "end": END},
    )
    workflow.add_conditional_edges(
        "call_tool",
        # Each agent node updates the 'sender' field# the tool calling node does not, meaning
        # this edge will route back to the original agent# who invoked the tool
        lambda x: x["sender"],
        {
            "researcher": "researcher",
            "chart_generator": "chart_generator",
        },
    )
    workflow.set_entry_point("researcher")
    graph = workflow.compile()
    return graph


def main(user_query: str, display: bool = True):
    graph = get_graph()
    if display:
        # from IPython.display import Image, display
        try:
            graph.get_graph().draw_mermaid_png(
                output_file_path="/home/churros/codes/agentes/grafo.png"
            )
            # display(Image(graph.get_graph().draw_mermaid_png()))
        except Exception:
            # This requires some extra dependencies and is optional
            pass

    # Invocando o grafo de estados
    events = graph.stream(
        {
            "messages": [("user", user_query)],
        },
        # Maximum number of steps to take in the graph
        {"recursion_limit": 10},
    )
    for s in events:
        print_pretty(s)
        print("----")


if __name__ == "__main__":
    # user_query = """Find the values of Brazil's GDP over the past 5 years  and make a line chart of it.
    #        Once you make the chart, save a file and finish."""
    #user_query = """Crie um gráfico representando uma função coseno, com valores entre -1 e 1.
    #        Quando estiver pronto, salve o arquivo e finalize."""
    user_query = """Encontre o valor do PIB per capita do Brasil nos últimos 5 anos. Em seguida crie um gráfico apresentando o resultado."""
    main(user_query)
