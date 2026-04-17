from langchain.agents.middleware import before_agent
from langgraph.runtime import Runtime

from edu_agent.context import EduAgentContext
from edu_agent.state import EduAgentState
from edu_agent.student import Student, get_student


@before_agent(state_schema=EduAgentState)
def load_student(_state: EduAgentState, runtime: Runtime[EduAgentContext]) -> dict[str, Student | None]:
    context = runtime.context
    student = get_student(context.user_id) if context.user_id else None
    return {"student": student}
