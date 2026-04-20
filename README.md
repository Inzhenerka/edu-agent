# Образовательный AI-агент

Чат-бот для студентов на базе LLM и FastAPI.

## Установка

Для управления зависимостями в проекте используется [uv](https://github.com/astral-sh/uv).

1. Установите `uv`, если он ещё не установлен.
2. Склонируйте репозиторий.
3. Установите зависимости:
   ```bash
   uv sync
   ```

## Настройка

1. Создайте файл `.env` в корне проекта или задайте переменную окружения:
   ```bash
   OPENAI_API_KEY=your_api_key_here
   ```
2. Настройки моделей, ролей и шаблонов находятся в `config.yml`.

## Запуск

Для запуска сервера используйте команду:

```bash
uv run fastapi dev
```

После запуска доступны:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- Demo UI: `http://127.0.0.1:8000/demo`

Для быстрой локальной проверки через `TestClient`:

```bash
uv run python main.py
```

## API

### `POST /ask`

Эндпоинт принимает `application/x-www-form-urlencoded` и возвращает JSON.

Поля формы:

- `role`: `math_tutor` или `history_tutor`
- `template`: `tutor_quick_answer` или `tutor_full_answer`
- `question`: вопрос пользователя
- `thread_id`: опциональный ID диалога; если передавать один и тот же, агент продолжит разговор

Пример запроса:

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "role=math_tutor" \
  -d "template=tutor_quick_answer" \
  -d "question=Что такое число Пи?" \
  -d "thread_id=lesson-1"
```

Пример ответа:

```json
{
  "content": "Ответ агента",
  "formula_solved": false,
  "thread_id": "lesson-1"
}
```

`formula_solved` показывает, использовал ли агент инструмент решения формулы.

### `GET /demo`

Возвращает простую HTML-страницу для ручного тестирования чата.
