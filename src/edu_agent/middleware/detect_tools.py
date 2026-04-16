from typing import Any
from langchain.agents.middleware import AgentMiddleware
from langgraph.runtime import Runtime

from edu_agent.state import EduAgentState
from edu_agent.utils import has_tool_call


class DetectedToolsMiddleware(AgentMiddleware):
    state_schema = EduAgentState

    def before_agent(self, state: EduAgentState, runtime: Runtime) -> dict[str, Any] | None:
        return {"formula_solved": False}

    def after_model(self, state: EduAgentState, runtime: Runtime) -> dict[str, Any] | None:
        if has_tool_call(state["messages"][-1], "solve_formula"):
            return {"formula_solved": True}
        return None
