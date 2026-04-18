from langchain.tools import BaseTool

from edu_agent.tools.formula import solve_formula
from edu_agent.tools.historical_period import detect_historical_period


def load_tools() -> list[BaseTool]:
    return [solve_formula, detect_historical_period]
