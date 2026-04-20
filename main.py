from loguru import logger
import sys

from edu_agent.agent import EduAgent, EduAgentContext

logger.remove()
logger.add(sys.stderr, level="INFO")

agent = EduAgent(llm_key="api", debug=False)

PROMPTS = [
    "Какой сейчас век?",
    "А до этого какой был?",
    "Перескажи наш диалог",
]

for prompt in PROMPTS:
    print(f"\n-> Запрос: {prompt}")
    response = agent.invoke(
        prompt=prompt,
        context=EduAgentContext(role="history_tutor", template="tutor_quick_answer"),
        thread_id='1',
    )
    print(f"Ответ: {response}")

print("\n-> Все сообщения из состояния")
messages = agent.get_messages(thread_id='1')
for m in messages:
    print(f"{m.type}: {m.content}")
