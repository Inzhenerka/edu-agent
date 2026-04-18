from typing import Callable
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

from edu_agent.context import EduAgentContext
from edu_agent.tools.formula import solve_formula
from edu_agent.tools.historical_period import detect_historical_period


@wrap_model_call
def select_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Удаляем ненужные инструменты в зависимости от роли."""
    # Извлекаем контекст
    context: EduAgentContext = request.runtime.context

    # Удаляем инструмент solve_formula для всех, кроме математика
    if context.role != "math_tutor":
        tools = [t for t in request.tools if t.name != solve_formula.name]
        request = request.override(tools=tools)
    elif context.role != "history_tutor":
        tools = [t for t in request.tools if t.name != detect_historical_period.name]
        request = request.override(tools=tools)

    return handler(request)
