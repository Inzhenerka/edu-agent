from langchain.tools import BaseTool

from edu_agent.tools.formula import solve_formula


def load_tools() -> list[BaseTool]:
    return [solve_formula]
