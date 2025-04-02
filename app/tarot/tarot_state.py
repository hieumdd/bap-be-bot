import operator
from typing import Annotated, TypedDict

from langchain.schema import AIMessage, HumanMessage

from app.tarot.tarot_telling_card_model import TarotTellingCard


class TarotState(TypedDict):
    messages: Annotated[list[HumanMessage | AIMessage], operator.add]
    tarot_telling_cards: Annotated[list[TarotTellingCard], operator.add]
    analysis: Annotated[list[str], operator.add]
    summary: str


class TarotAnalyzeState(TypedDict):
    question: str
    tarot_telling_card: TarotTellingCard
