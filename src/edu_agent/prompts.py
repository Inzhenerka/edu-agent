from typing import ClassVar
from pathlib import Path
from pydantic import BaseModel
from jinja2 import Template, StrictUndefined

from edu_agent.config import RoleType, TemplateType, ToneType


class BasePrompt(BaseModel):
    __file_path__: ClassVar[str | Path]

    def render_prompt(self) -> str:
        text = Path(self.__file_path__).read_text(encoding="utf-8")
        template = Template(text, undefined=StrictUndefined)
        return template.render(self.model_dump()).strip()


class BaseTemplatePrompt(BasePrompt):
    role_instruction: str
    tone_instruction: str
    context_instructions: list[str] | None = None


class BaseRolePrompt(BasePrompt):
    pass


class BaseContextPrompt(BasePrompt):
    pass


class BaseTonePrompt(BasePrompt):
    pass


class TutorFullAnswerPrompt(BaseTemplatePrompt):
    __file_path__ = "prompts/templates/tutor_full_answer.jinja"


class TutorQuickAnswerPrompt(BaseTemplatePrompt):
    __file_path__ = "prompts/templates/tutor_quick_answer.jinja"


class MathTutorPrompt(BaseRolePrompt):
    __file_path__ = "prompts/roles/math_tutor.jinja"


class HistoryTutorPrompt(BaseRolePrompt):
    __file_path__ = "prompts/roles/history_tutor.jinja"


class FormulaSolutionPrompt(BaseContextPrompt):
    __file_path__ = "prompts/context/formula_solution.jinja"


class FriendlyTonePrompt(BaseTonePrompt):
    __file_path__ = "prompts/tones/friendly.jinja"


class FormalTonePrompt(BaseTonePrompt):
    __file_path__ = "prompts/tones/formal.jinja"


def render_system_instructions(role: RoleType, template: TemplateType, tone: ToneType) -> str:
    match role:
        case "math_tutor":
            role_instruction: str = MathTutorPrompt().render_prompt()
            context_instructions: list[str] = [FormulaSolutionPrompt().render_prompt()]
        case "history_tutor":
            role_instruction = HistoryTutorPrompt().render_prompt()
            context_instructions = []
        case _:
            raise ValueError(f"Unknown role: {role}")
    match tone:
        case "friendly":
            tone_instruction = FriendlyTonePrompt().render_prompt()
        case "formal":
            tone_instruction = FormalTonePrompt().render_prompt()
        case _:
            raise ValueError(f"Unknown tone: {tone}")
    match template:
        case "tutor_full_answer":
            return TutorFullAnswerPrompt(
                role_instruction=role_instruction,
                tone_instruction=tone_instruction,
                context_instructions=context_instructions
            ).render_prompt()
        case "tutor_quick_answer":
            return TutorQuickAnswerPrompt(
                role_instruction=role_instruction,
                tone_instruction=tone_instruction,
                context_instructions=context_instructions
            ).render_prompt()
        case _:
            raise ValueError(f"Unknown template: {template}")
