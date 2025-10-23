from io import StringIO
from textwrap import dedent

from langchain.messages import AIMessage, SystemMessage
from langgraph.types import Send
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

from app.bot.message import FileMessage, ImageMessage, TextMessage
from app.core.chat_model import ChatModelService, ChatModelNode
from app.ziwei.ziwei_model import ZiweiArcAnalysis, ZiweiBirthchart
from app.ziwei.ziwei_state import ZiweiArcAnalysisState, ZiweiTellingState, ZiweiSummaryState


class ExtractZiweiBirthchart(ChatModelNode):
    chat_model_service: ChatModelService
    system_message = SystemMessage(content="Parse the following Vietnamese date and time and gender")
    human_message = HumanMessagePromptTemplate.from_template("{message}")
    prompt = ChatPromptTemplate.from_messages([system_message, human_message])

    def __call__(self, state: ZiweiTellingState):
        chain = self.prompt | self.chat_model_service.chat_model.with_structured_output(ZiweiBirthchart)
        birthchart: ZiweiBirthchart = chain.invoke(state["messages"][-1].content)
        return ZiweiTellingState(birthchart=birthchart)


class ValidateZiweiBirthchart:
    def __call__(self, state: ZiweiTellingState):
        return state["birthchart"].error


class HandleZiweiBirthchartError:
    def __call__(self, _: ZiweiTellingState):
        content = "Xin lỗi, tôi không thể hiểu được thông tin ngày sinh của bạn.\nVui lòng cung cấp ngày sinh theo định dạng: ngày/tháng/năm giờ:phút và giới tính của bạn."
        return ZiweiTellingState(messages=[AIMessage(content=content)], bot_messages=[TextMessage(content)])


class DumpZiweiBirthchartImage:
    def __call__(self, state: ZiweiTellingState):
        return ZiweiTellingState(bot_messages=[ImageMessage(state["birthchart"].image, "Lá số Tử Vi")])


class MapAnalyzeZiweiArcs:
    node_id: str
    arcs = [
        "Mệnh",
        "Phụ Mẫu",
        "Phúc Đức",
        "Điền Trạch",
        "Quan Lộc",
        "Nô Bộc",
        "Thiên Di",
        "Tật Ách",
        "Tài Bạch",
        "Tử Tức",
        "Phu Thê",
        "Huynh Đệ",
    ]

    def __init__(self, node_id: str):
        self.node_id = node_id

    def __call__(self, state: ZiweiTellingState):
        return [Send(self.node_id, ZiweiArcAnalysisState(birthchart=state["birthchart"], arc=arc)) for arc in self.arcs]


class AnalyzeZiweiArc(ChatModelNode):
    system_message = SystemMessage(
        content=dedent(
            """
            Bạn là một nhà chiêm tinh và chuyên gia tử vi đẩu số Việt Nam. Sử dụng lá số tử vi đẩu số sau đây làm ngữ cảnh, hãy phân tích và đưa ra những nhận định về lá số này.
            Phân tích cần dựa trên kiến thức phong thủy và tử vi đẩu số truyền thống Việt Nam, kết hợp giữa các yếu tố âm dương, ngũ hành, cung mệnh và con giáp.
            Hãy phân tích chi tiết về Cung được nêu trong trong yêu cầu. Đầu tiên, hãy xác định đúng ô (cung) cần tìm, sau đó phân tích các sao, vị trí của sao, tương tác giữa các sao.
            Khi trả lời, chỉ đưa ra phân tích, không đưa ra giới thiệu về cung. Ngoài ra không đưa ra thông tin gì thêm
            Đưa ra Kết quả phân tích theo định dạng
            Cung: <cung>
            Phân tích: <phân tích>
            """
        )
    )
    human_message = HumanMessagePromptTemplate.from_template(
        template=[
            {"type": "text", "text": "Phân tích Cung {arc}"},
            {"type": "image_url", "image_url": "{image}"},
        ]
    )
    prompt = ChatPromptTemplate.from_messages([system_message, human_message])

    def __call__(self, state: ZiweiArcAnalysisState):
        arc = state["arc"]
        chain = self.prompt | self.chat_model_service.chat_model
        message: AIMessage = chain.invoke({"arc": state["arc"], "image": state["birthchart"].image_b64})
        return ZiweiTellingState(messages=[message], analyses=[ZiweiArcAnalysis(arc=arc, analysis=message.content)])


class DumpZiweiArcAnalysis:
    def __call__(self, state: ZiweiTellingState):
        fo = StringIO()
        for analysis in state["analyses"]:
            fo.write(analysis.analysis)
            fo.write("\n\n")
        fo.seek(0)
        return ZiweiTellingState(analysis_file=fo, bot_messages=[FileMessage("ziwei.txt", fo, "Luận giải chi tiết")])


class MapSummarizeZiwei:
    node_id: str
    sentiments: list[str] = [
        "tích cực",
        "tiêu cực",
        "lời khuyên",
    ]

    def __init__(self, node_id: str):
        self.node_id = node_id

    def __call__(self, state: ZiweiTellingState):
        return [Send(self.node_id, ZiweiSummaryState(analyses=state["analyses"], sentiment=sentiment)) for sentiment in self.sentiments]


class SummarizeZiwei(ChatModelNode):
    system_message = SystemMessagePromptTemplate.from_template(
        dedent(
            """
            Bạn là một nhà chiêm tinh và chuyên gia tử vi đẩu số Việt Nam.
            Ở tin nhắn trước bạn đã phân tích tất cả các Cung của 1 lá số của một người.
            Hãy sử dụng ngữ cảnh được cung cấp (phân tích các Cung của lá số)
            Đưa ra 5 điểm {sentiment} nhất, giải thích theo ngôn ngữ dễ hiểu.
            Trả lời theo bullet points, đúng 5 bullet points
            """
        )
    )
    prompt = ChatPromptTemplate.from_messages([system_message])

    def __call__(self, state: ZiweiSummaryState):
        for analysis in state["analyses"]:
            human_message = HumanMessagePromptTemplate.from_template(analysis.analysis)
            self.prompt.extend([human_message])
        chain = self.prompt | self.chat_model_service.chat_model
        message: AIMessage = chain.invoke({"sentiment": state["sentiment"]})
        return ZiweiTellingState(messages=[message], summaries=[message.content], bot_messages=[TextMessage(message.content)])
