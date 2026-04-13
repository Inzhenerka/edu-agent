from langchain.tools import BaseTool

from edu_agent.config import RoleType
from edu_agent.tools.formula import solve_formula


def load_tools(role: RoleType) -> list[BaseTool]:
    match role:
        case "math_tutor":
            return [solve_formula]
        case "history_tutor":
            return []
        case _:
            raise ValueError(f"Unknown role: {role}")
