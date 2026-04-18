from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph
from langchain.messages import HumanMessage
from langchain.agents.middleware import ModelRetryMiddleware, ModelCallLimitMiddleware
from pydantic import BaseModel

from edu_agent.config import Config
from edu_agent.chat_model import load_chat_model
from edu_agent.tools.load_tools import load_tools
from edu_agent.tools.historical_period import HistoricalPeriodType
from edu_agent.context import EduAgentContext
from edu_agent.middleware.system_instructions import system_instructions
from edu_agent.middleware.select_tools import select_tools
from edu_agent.middleware.filter_profanity import filter_profanity
from edu_agent.middleware.detect_tools import DetectedToolsMiddleware

# Загружаем ключ из .env-файла
load_dotenv()


class EduAgentResponse(BaseModel):
    content: str
    formula_solved: bool
    historical_period: HistoricalPeriodType | None

    def __str__(self) -> str:
        content = self.content.strip()
        content += f"\n* Формула решена" if self.formula_solved else ""
        content += f"\n* Исторический период: {self.historical_period}" if self.historical_period else ""
        return content


class EduAgent:
    _agent: CompiledStateGraph

    def __init__(self, llm_key: str, debug: bool = False):
        # Загружаем конфигурацию
        config = Config.from_yaml_file("config.yml")
        llm_config = config.llms[llm_key]

        # Создаем модель чата
        chat_model = load_chat_model(llm_config=llm_config)

        # Создаем агента ReAct
        self._agent = create_agent(
            model=chat_model,
            debug=debug,
            tools=load_tools(),
            context_schema=EduAgentContext,
            middleware=[
                DetectedToolsMiddleware(),
                ModelRetryMiddleware(max_retries=2, initial_delay=1),
                ModelCallLimitMiddleware(run_limit=4, exit_behavior="end"),
                filter_profanity,
                system_instructions,
                select_tools,
            ],
        )

    def invoke(self, prompt: str, context: EduAgentContext) -> EduAgentResponse:
        """Вызываем агента и извлекаем ответ из массива сообщений"""
        # Ограничиваем длину запроса для экономии токенов
        prompt = prompt.strip()[:4000]
        # Формируем и передаем агенту сообщение
        response = self._agent.invoke(input={"messages": HumanMessage(prompt)}, context=context)
        # Формируем ответ из последнего сообщения и состояния
        return EduAgentResponse(
            content=response['messages'][-1].content,
            formula_solved=response.get('formula_solved', False),
            historical_period=response.get('historical_period')
        )
