from edu_agent.agent import EduAgent

# Создаем агента
agent = EduAgent(llm_key="api", role="math_tutor", template="tutor_quick_answer")

# Вызываем его, получая текстовый ответ
response = agent.invoke(prompt="Посчитай 1+1/2-0,5-(3/2-3/6)")

# Выводим ответ
print(response)
