from typing import Annotated

from langchain_tavily import TavilySearch
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL

tavily_tool = TavilySearch(max_results=5)
duckduckgo_tool = DuckDuckGoSearchRun(max_results=3)

# Warning: This executes code locally, which can be unsafe when not sandboxed
repl = PythonREPL()


@tool
def python_repl_tool(
    code: Annotated[str, "The python code to execute to generate your chart."],
):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return (
        result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."
    )


def print_pretty(event):
    """Pretty-print the event messages for debugging or logging purposes.

    Args:
        event (dict): The event containing messages from the research or chart node.
    """
    # Check if the event contains 'research_node' or 'chart_node'
    for node_key in ["research_node", "chart_node"]:
        if node_key in event:
            messages = event[node_key].get("messages", [])
            print(f"{node_key}: [")
            for message in messages:
                # Extract message type (HumanMessage, AIMessage, etc.)
                message_type = message.__class__.__name__
                content = message.content
                if isinstance(content, list):
                    content = [
                        item for item in content
                    ]  # Handle list content (e.g., AIMessage with tool use)
                elif isinstance(content, str):
                    content = f'"{content}"'  # Wrap string content in quotes
                # Extract additional fields
                additional_kwargs = message.additional_kwargs
                response_metadata = message.response_metadata
                message_id = message.id
                # Print the message in the desired format
                print(f"    {message_type}(")
                print(f"        content={content},")
                print(f"        additional_kwargs={additional_kwargs},")
                print(f"        response_metadata={response_metadata},")
                print(f"        id='{message_id}'")
                print("    ),")
            print("]")
            print("-" * 120)
            return
    print("No messages found in the event.")
