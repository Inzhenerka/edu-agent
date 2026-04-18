from typing import Annotated, Literal, cast, get_args

from langchain.tools import tool
from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId
from langgraph.types import Command

type HistoricalPeriodType = Literal[
    "prehistory",
    "ancient_world",
    "middle_ages",
    "modern_period",
    "contemporary_period",
]


def normalize_historical_period(value: str) -> HistoricalPeriodType | None:
    normalized_value = value.strip().lower()
    if normalized_value in get_args(HistoricalPeriodType.__value__):
        return cast(HistoricalPeriodType, normalized_value)
    return None


@tool
def detect_historical_period(
    historical_period: HistoricalPeriodType, tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """
    Детектор исторического периода, о котором упоминает в сообщении человек.
    Вызывай инструмент в тех случаях, когда можно уверенно понять, о каком периоде идет речь, чтобы его залогировать.

    Аргументы:
        historical_period: одно из допустимых обозначений исторического периода
    """
    normalized_period = normalize_historical_period(historical_period)

    tool_message_content = (
        f"Исторический период: {normalized_period}" if normalized_period else "Исторический период не распознан"
    )

    return Command(
        update={
            "historical_period": normalized_period,
            "messages": [ToolMessage(content=tool_message_content, tool_call_id=tool_call_id)],
        }
    )
