from langchain.messages import AnyMessage
from safetext import SafeText


def has_profanity(text: str) -> bool:
    """Проверка текста на нецензурную брань."""
    st = SafeText(language=None)
    st.set_language_from_text(text)
    results = st.check_profanity(text=text)
    return bool(results)


def has_tool_call(message: AnyMessage, tool_name: str) -> bool:
    tool_calls = getattr(message, "tool_calls", None) or []
    return any(tc.get("name") == tool_name for tc in tool_calls)
