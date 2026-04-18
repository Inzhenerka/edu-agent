from typing import NotRequired
from langchain.agents import AgentState

from edu_agent.tools.historical_period import HistoricalPeriodType


class EduAgentState(AgentState):
    formula_solved: NotRequired[bool]
    historical_period: NotRequired[HistoricalPeriodType | None]
