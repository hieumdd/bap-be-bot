import operator
from typing import Annotated, TypedDict

from langchain.schema import AIMessage, HumanMessage

from app.bot.message import BotMessage
from app.tarot.tarot_card_model import TarotCard


class TarotTellingState(TypedDict):
    tarot_cards: Annotated[list[TarotCard], operator.add]
    messages: Annotated[list[HumanMessage | AIMessage], operator.add]
    bot_messages: Annotated[list[BotMessage], operator.add]


class TarotCardAnalyzeState(TypedDict):
    question: str
    tarot_card: TarotCard
