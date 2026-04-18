from edu_agent.agent import EduAgent, EduAgentContext

agent = EduAgent(llm_key="api", debug=False)

PROMPTS = [
    "Когда было смутное время?",
    "Почему пала Римская Империя?",
    "Как стать историком?"
]

for prompt in PROMPTS:
    print(f"\n-> Запрос: {prompt}")
    response = agent.invoke(
        prompt=prompt,
        context=EduAgentContext(role="history_tutor", template="tutor_quick_answer")
    )
    print(f"Ответ: {response}")
