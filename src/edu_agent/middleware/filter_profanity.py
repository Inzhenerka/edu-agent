from typing import Any
from langchain.agents.middleware import before_agent, hook_config, AgentState
from langchain.messages import AIMessage
from langgraph.runtime import Runtime

from edu_agent.utils import has_profanity


@before_agent
@hook_config(can_jump_to=["end"])
def filter_profanity(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    if has_profanity(state["messages"][-1].content):
        return {
            "messages": [AIMessage("Я не могу ответить на такой запрос.")],
            "jump_to": "end"
        }
    return None
