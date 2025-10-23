import operator
from typing import Annotated, Sequence

from langgraph.graph import MessagesState

from app.bot.message import BotMessage


class BotMessagesState(MessagesState):
    bot_messages: Annotated[Sequence[BotMessage], operator.add]
