from fastapi.testclient import TestClient
from edu_agent.api import app, EduAgentResponse

PROMPTS = [
    "Какой сейчас век?",
    "А до этого какой был?",
    "Перескажи наш диалог",
]

with TestClient(app) as client:
    for prompt in PROMPTS:
        print(f"\n-> Запрос: {prompt}")
        response = client.post(
            "/ask",
            data={
                "role": "history_tutor",
                "template": "tutor_quick_answer",
                "question": prompt,
                "thread_id": "1",
            },
        )
        agent_response = EduAgentResponse.model_validate(response.json())
        print(f"Ответ: {agent_response.content}")
