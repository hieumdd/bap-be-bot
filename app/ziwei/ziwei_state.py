from io import BytesIO
import operator
from typing import Annotated, TypedDict

from langchain.schema import AIMessage, HumanMessage

from app.ziwei.ziwei_model import ZiweiInput


class ZiweiState(TypedDict):
    messages: Annotated[list[HumanMessage | AIMessage], operator.add]

    birthchart_input: ZiweiInput | None = None
    birthchart_image_b64: str | None = None
    birthchart_image: BytesIO | None = None

    analysis_menh: str | None = None
    analysis_phu_mau: str | None = None
    analysis_phuc_duc: str | None = None
    analysis_dien_trach: str | None = None
    analysis_quan_loc: str | None = None
    analysis_no_boc: str | None = None
    analysis_thien_di: str | None = None
    analysis_tat_ach: str | None = None
    analysis_tai_bach: str | None = None
    analysis_tu_tuc: str | None = None
    analysis_phu_the: str | None = None
    analysis_huynh_de: str | None = None

    summary: str | None = None

    error: str | None = None
