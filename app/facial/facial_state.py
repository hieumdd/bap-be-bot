import operator
from typing import Annotated, TypedDict

from langchain.schema import AIMessage, HumanMessage

from app.bot.message import BotMessage
from app.facial.facial_model import FacialFeatures


class FacialTellingState(TypedDict):
    messages: Annotated[list[HumanMessage | AIMessage], operator.add]
    image_url: str
    facial_features: FacialFeatures
    bot_messages: Annotated[list[BotMessage], operator.add]
