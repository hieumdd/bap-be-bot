import operator
from typing import Annotated, TypedDict

from langchain.schema import AIMessage, HumanMessage

from app.bot.message import BotMessage
from app.ziwei.ziwei_model import ZiweiArcAnalysis, ZiweiBirthchart


class ZiweiTellingState(TypedDict):
    messages: Annotated[list[HumanMessage | AIMessage], operator.add]
    birthchart: ZiweiBirthchart
    analyses: Annotated[list[ZiweiArcAnalysis], operator.add]
    summaries: Annotated[list[str], operator.add]
    bot_messages: Annotated[list[BotMessage], operator.add]


class ZiweiArcAnalysisState(TypedDict):
    birthchart: ZiweiBirthchart
    arc: str


class ZiweiSummaryState(TypedDict):
    sentiment: str
    analyses: list[ZiweiArcAnalysis]
