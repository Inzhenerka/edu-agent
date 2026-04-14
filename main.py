from edu_agent.agent import EduAgent, EduAgentContext

agent = EduAgent(llm_key="api", debug=False)

PROMPTS = [
    "Посчитай 1+2*2",
    "Один плюс два умножить на три корня из трех это сколько?",
    "Это правильное выражение? sqrt(2)-1+x^2. Если да, то преобразуй"
]

for prompt in PROMPTS:
    print(f"\n-> Запрос: {prompt}")
    response = agent.invoke(
        prompt=prompt,
        context=EduAgentContext(role="math_tutor", template="tutor_quick_answer")
    )
    print(f"Ответ: {response}")
