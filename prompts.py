chart_task = """Create clear and visually appealing charts using seaborn and plotly. Follow these rules:
1. Add a title, labeled axes (with units), and a legend if needed.
2. Use `sns.set_context("notebook")` for readable text and themes like `sns.set_theme()` or `sns.set_style("whitegrid")`.
3. Use accessible color palettes like `sns.color_palette("husl")`.
4. Choose appropriate plots: `sns.lineplot()`, `sns.barplot()`, or `sns.heatmap()`.
5. Annotate key points (e.g., "Peak in 2020") for clarity.
6. Ensure the chart's width and display resolution is no wider than 1000px.
7. Display with `plt.show()`.
8. Save in the current directory (/home/churros/codes/agentes/appropriate_name.pdf) with `plt.savefig(appropriate_name.pdf)`

Goal: Produce accurate, engaging, and easy-to-interpret charts."""


## System prompt
def make_system_prompt(suffix: str) -> str:
    return (
        "You are a helpful AI assistant, collaborating with other assistants."
        " Use the provided tools to progress towards answering the question."
        " If you are unable to fully answer, that's OK, another assistant with different tools "
        " will help where you left off. Execute what you can to make progress."
        " If you or any of the other assistants have the final answer or deliverable,"
        " prefix your response with FINAL ANSWER so the team knows to stop."
        f"\n{suffix}"
    )
