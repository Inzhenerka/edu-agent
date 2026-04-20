from contextlib import asynccontextmanager
from loguru import logger
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse

from edu_agent.agent import EduAgentContext, EduAgentResponse
from edu_agent.config import RoleType, TemplateType
from edu_agent.dependencies import init_global_dependencies, EduAgentDependency


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_global_dependencies(app)
    logger.info("Starting agent")
    yield
    logger.info("Stopping agent")


app = FastAPI(lifespan=lifespan)


@app.get('/demo')
def demo():
    """Simple demo of web UI."""
    return FileResponse("templates/demo.html")


@app.post('/ask')
def ask(
    edu_agent: EduAgentDependency,
    role: RoleType = Form(description="Role of AI assistant"),
    template: TemplateType = Form(description="Response format"),
    question: str = Form(description="Student question", examples=["Ты кто?"]),
    thread_id: str | None = Form(default=None, description="Chat thread id"),
) -> EduAgentResponse:
    """Ask question to educational agent."""
    try:
        return edu_agent.invoke(
            prompt=question,
            context=EduAgentContext(role=role, template=template),
            thread_id=thread_id,
        )
    except Exception as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
