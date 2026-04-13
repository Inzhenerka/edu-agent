from dotenv import load_dotenv
from loguru import logger
from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph
from langchain.messages import HumanMessage

from edu_agent.config import Config, RoleType, TemplateType
from edu_agent.chat_model import load_chat_model
from edu_agent.prompts import render_system_instructions

# Загружаем ключ из .env-файла
load_dotenv()


class EduAgent:
    _agent: CompiledStateGraph

    def __init__(self, llm_key: str, role: RoleType, template: TemplateType, debug: bool = False):
        # Загружаем конфигурацию
        config = Config.from_yaml_file("config.yml")
        llm_config = config.llms[llm_key]

        # Создаем модель чата
        chat_model = load_chat_model(llm_config=llm_config)

        # Рендерим системную инструкцию
        instructions = render_system_instructions(role=role, template=template)
        logger.debug(f"LLM instructions: {instructions}")

        # Создаем агента ReAct
        self._agent = create_agent(
            model=chat_model,
            system_prompt=instructions,
            debug=debug,
        )

    def invoke(self, prompt: str) -> str:
        """Вызываем агента и извлекаем ответ из массива сообщений"""
        response = self._agent.invoke(input={"messages": HumanMessage(prompt)})
        return response['messages'][-1].content
