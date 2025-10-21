import operator
from typing import Annotated, TypedDict

from langchain.schema import AIMessage, HumanMessage

from app.tarot.tarot_card_model import TarotCard


class TarotTellingState(TypedDict):
    messages: Annotated[list[HumanMessage | AIMessage], operator.add]
    tarot_cards: Annotated[list[TarotCard], operator.add]
    analysis: Annotated[list[str], operator.add]
    summary: str


class TarotCardAnalyzeState(TypedDict):
    question: str
    tarot_card: TarotCard
