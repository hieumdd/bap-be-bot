from typing import Annotated, TypedDict
import operator

from langchain.schema import AIMessage, HumanMessage


class RagState(TypedDict):
    messages: Annotated[list[HumanMessage | AIMessage], operator.add]
