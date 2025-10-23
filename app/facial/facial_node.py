from textwrap import dedent

from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

from app.bot.message import TextMessage
from app.core.chat_model import ChatModelNode
from app.facial.facial_model import FacialFeatures
from app.facial.facial_state import FacialTellingState


class ExtractFacialFeatures(ChatModelNode):
    system_message = SystemMessage(
        content=dedent("""
            Bạn là một chuyên viên mô tả khuôn mặt.
            Nhiệm vụ của bạn là quan sát ảnh khuôn mặt người và **mô tả chi tiết các đặc điểm vật lý** mà bạn nhìn thấy, KHÔNG giải thích ý nghĩa tướng học.
            Đầu vào: Một ảnh khuôn mặt người (rõ ràng, chính diện).
            Đầu ra: JSON chứa mô tả chi tiết các bộ phận khuôn mặt.

            ## Quy tắc:
            1. Ghi nhận từng đặc điểm ở mức mô tả trung lập, không phán đoán hay diễn giải.
            2. Không thêm bình luận, cảm xúc, hoặc phân tích tính cách.
            3. Nếu ảnh bị mờ hoặc không đủ thông tin, hãy trả về lỗi.
            """)
    )
    human_message = HumanMessagePromptTemplate.from_template(
        template=[
            {"type": "text", "text": "Hãy phân tích chân dung sau"},
            {"type": "image_url", "image_url": "{image}"},
        ]
    )
    prompt = ChatPromptTemplate.from_messages([system_message, human_message])

    def __call__(self, state: FacialTellingState):
        chain = self.prompt | self.chat_model_service.chat_model.with_structured_output(FacialFeatures)
        facial_features: FacialFeatures = chain.invoke({"image": state["image_url"]})
        return FacialTellingState(facial_features=facial_features)


class ValidateFacialFeatures:
    def __call__(self, state: FacialTellingState):
        return state["facial_features"].error


class HandleFacialFeaturesExtractionError:
    def __call__(self, _: FacialTellingState):
        content = "Xin lỗi, tôi không thể hiểu được ảnh này."
        return FacialTellingState(messages=[AIMessage(content=content)], bot_messages=[TextMessage(content)])


class DumpFacialFeatures:
    def __call__(self, state: FacialTellingState):
        return FacialTellingState(bot_messages=[TextMessage(state["facial_features"].model_dump_json())])


class AnalyzeFacialFeatures(ChatModelNode):
    system_message = SystemMessage(
        content=dedent(
            """
            Bạn là chuyên gia tướng học Việt Nam, am hiểu nhân tướng học Á Đông.
            Dưới đây là các đặc điểm khuôn mặt của một người. Hãy dựa vào đó để phân tích ý nghĩa tướng học tổng thể, bao gồm:
            - Tính cách
            - Công danh, sự nghiệp
            - Tình duyên
            - Sức khỏe
            - Vận mệnh chung (ngắn hạn và dài hạn)

            Hãy viết bài phân tích chi tiết, giàu nội dung, tự nhiên, và mang phong cách của người xem tướng — có thể sử dụng văn phong tướng số Việt Nam.
            Văn bản trả ra dưới 2000 ký tự
            """
        )
    )
    human_message = HumanMessagePromptTemplate.from_template(template=[{"type": "text", "text": "Đầu vào: {input}"}])
    prompt = ChatPromptTemplate.from_messages([system_message, human_message])

    def __call__(self, state: FacialTellingState):
        chain = self.prompt | self.chat_model_service.chat_model
        analysis: AIMessage = chain.invoke({"input": state["facial_features"].model_dump_json(indent=2)})
        return FacialTellingState(messages=[analysis], bot_messages=[TextMessage(analysis.content)])
