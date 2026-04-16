from typing import NotRequired
from langchain.agents import AgentState


class EduAgentState(AgentState):
    formula_solved: NotRequired[bool]
