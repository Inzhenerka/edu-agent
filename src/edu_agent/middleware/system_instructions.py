from langchain.agents.middleware import dynamic_prompt, ModelRequest
from loguru import logger

from edu_agent.context import EduAgentContext
from edu_agent.prompts import render_system_instructions
from edu_agent.state import EduAgentState


@dynamic_prompt
def system_instructions(request: ModelRequest[EduAgentContext]) -> str:
    # Извлекаем контекст
    context: EduAgentContext = request.runtime.context

    # Извлекаем из запроса состояние
    state: EduAgentState = request.state
    student = state.get("student")

    # Рендерим системную инструкцию
    instructions = render_system_instructions(
        role=context.role,
        template=context.template,
        tone=student.tone if student else "formal",
    )
    logger.debug(f"LLM instructions: {instructions}")

    return instructions
