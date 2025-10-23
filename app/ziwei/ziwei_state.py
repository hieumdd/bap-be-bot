import operator
from typing import Annotated, TypedDict

from app.core.state import BotMessagesState
from app.ziwei.ziwei_model import ZiweiArcAnalysis, ZiweiBirthchart


class ZiweiTellingState(BotMessagesState):
    birthchart: ZiweiBirthchart
    analyses: Annotated[list[ZiweiArcAnalysis], operator.add]
    summaries: Annotated[list[str], operator.add]


class ZiweiArcAnalysisState(TypedDict):
    birthchart: ZiweiBirthchart
    arc: str


class ZiweiSummaryState(TypedDict):
    sentiment: str
    analyses: list[ZiweiArcAnalysis]
