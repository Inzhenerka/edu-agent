from typing import Annotated
import sys
import os
from loguru import logger
from fastapi import FastAPI, Request, Depends
from dotenv import load_dotenv

from edu_agent.agent import EduAgent


def init_global_dependencies(app: FastAPI):
    # Загрузка переменных из .env
    load_dotenv()
    # Настройка глобального логгера
    logger_level = os.getenv("LOG_LEVEL", "DEBUG")
    logger.remove()
    logger.add(sys.stdout, level=logger_level)
    # Создание агента
    app.state.edu_agent = EduAgent(llm_key="api", debug=False)


def get_edu_agent(request: Request) -> EduAgent:
    return request.app.state.edu_agent


type EduAgentDependency = Annotated[EduAgent, Depends(get_edu_agent)]
