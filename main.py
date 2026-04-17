from edu_agent.agent import EduAgent, EduAgentContext

agent = EduAgent(llm_key="api", debug=False)

PROMPTS = [
    "Кому на Руси жить хорошо?"
]

for prompt in PROMPTS:
    print(f"\n-> Запрос: {prompt}")
    response = agent.invoke(
        prompt=prompt,
        context=EduAgentContext(role="history_tutor", template="tutor_quick_answer", tone="friendly")
    )
    print(f"Ответ: {response}")
