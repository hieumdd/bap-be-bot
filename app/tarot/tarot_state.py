import operator
from typing import Annotated, TypedDict

from app.core.state import BotMessagesState
from app.tarot.tarot_card_model import TarotCard


class TarotTellingState(BotMessagesState):
    tarot_cards: Annotated[list[TarotCard], operator.add]


class TarotCardAnalyzeState(TypedDict):
    question: str
    tarot_card: TarotCard
