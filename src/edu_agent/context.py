from pydantic import BaseModel

from edu_agent.config import RoleType, TemplateType, ToneType


class EduAgentContext(BaseModel):
    role: RoleType
    template: TemplateType
    tone: ToneType = "formal"
