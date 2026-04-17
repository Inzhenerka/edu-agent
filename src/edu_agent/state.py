from typing import NotRequired
from langchain.agents import AgentState

from edu_agent.student import Student


class EduAgentState(AgentState):
    formula_solved: NotRequired[bool]
    student: NotRequired[Student | None]
