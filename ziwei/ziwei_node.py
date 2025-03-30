from textwrap import dedent

from langchain.schema import SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

from rag import chat_model
from ziwei.ziwei_model import ZiweiInput
from ziwei.ziwei_service import generate_ziwei_image
from ziwei.ziwei_state import ZiweiState


def extract_input(state: ZiweiState) -> dict:
    """Use LLM to extract birthdate, time, and gender from the user input in Vietnamese"""
    messages = state["messages"]
    system_message = SystemMessage(
        content="Parse the following Vietnamese date and time and gender"
    )
    human_message = HumanMessagePromptTemplate.from_template("{message}")
    prompt = ChatPromptTemplate.from_messages([system_message, human_message])
    chain = prompt | chat_model.with_structured_output(ZiweiInput)
    input_ = chain.invoke(messages[-1].content)
    return {"birthchart_input": input_}


def handle_error(state: ZiweiState) -> dict:
    """Handle error when input extraction fails"""
    error_message = AIMessage(
        content=dedent(
            """
            Xin lỗi, tôi không thể hiểu được thông tin ngày sinh của bạn.
            Vui lòng cung cấp ngày sinh theo định dạng: ngày/tháng/năm giờ:phút và giới tính của bạn.
            """
        )
    )
    return {
        "messages": state["messages"] + [error_message],
        "error": "Input extraction failed",
    }


def generate_image(state: ZiweiState) -> dict:
    """Generate birth chart image based on birthdate and gender"""
    ziwei_input = state["birthchart_input"]
    image_b64, image = generate_ziwei_image(ziwei_input)
    return {"birthchart_image_b64": image_b64, "birthchart_image": image}


def create_analyze(arc: str, arc_key: str):
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

    def analyze(state: ZiweiState) -> dict:
        """Let the LLM perform analysis using the image as context"""
        image = state["birthchart_image_b64"]
        prompt = ChatPromptTemplate.from_messages([system_message, human_message])
        chain = prompt | chat_model
        analysis: AIMessage = chain.invoke({"arc": arc, "image": image})
        return {"messages": state["messages"] + [analysis], arc_key: analysis.content}

    return analyze


analyze_menh = create_analyze("Mệnh", "analysis_menh")
analyze_phu_mau = create_analyze("Phụ Mẫu", "analysis_phu_mau")
analyze_phuc_duc = create_analyze("Phúc Đức", "analysis_phuc_duc")
analyze_dien_trach = create_analyze("Điền Trạch", "analysis_dien_trach")
analyze_quan_loc = create_analyze("Quan Lộc", "analysis_quan_loc")
analyze_no_boc = create_analyze("Nô Bộc", "analysis_no_boc")
analyze_thien_di = create_analyze("Thiên Di", "analysis_thien_di")
analyze_tat_ach = create_analyze("Tật Ách", "analysis_tat_ach")
analyze_tai_bach = create_analyze("Tài Bạch", "analysis_tai_bach")
analyze_tu_tuc = create_analyze("Tử Tức", "analysis_tu_tuc")
analyze_phu_the = create_analyze("Phu Thê", "analysis_phu_the")
analyze_huynh_de = create_analyze("Huynh Đệ", "analysis_huynh_de")
