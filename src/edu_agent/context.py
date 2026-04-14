from pydantic import BaseModel

from edu_agent.config import RoleType, TemplateType


class EduAgentContext(BaseModel):
    role: RoleType
    template: TemplateType
