from dependency_injector import containers, providers
from langchain_core.prompts import PromptTemplate


MESSAGE = PromptTemplate.from_template(
    """
    Bạn là 1 người đang tổng hợp lại các tin nhắn được nhắn trong một nhóm trò chuyện giữa những người bạn.
    Dưới đây là một số tin nhắn có liên quan đến câu hỏi.

    --- Tin nhắn ---
    {context}
    --- Hết tin nhắn ---

    Câu hỏi: {query}

    Hãy phân tích tình huống và đưa ra câu trả lời dựa trên thông tin từ tin nhắn trên.
    Yêu cầu đối với câu trả lời:
    - Không sử dụng markdown, nhưng có thể sử dụng các kí hiệu.
    - Mỗi đoạn văn không quá 4096 ký tự.
    - Các gạch đầu dòng phải nối tiếp nhau, không có xuống dòng.
    """
)

CONVERSATION = PromptTemplate.from_template(
    """
    Bạn là 1 người đang tổng hợp lại các tin nhắn được nhắn trong một nhóm trò chuyện giữa những người bạn.
    Dưới đây là một số cuộc hội thoại có liên quan đến câu hỏi. Mỗi cuộc hội thoại bắt đầu bằng <CONVERSATION> và kết thúc bằng </CONVERSATION>

    --- Tin nhắn ---
    {context}
    --- Hết tin nhắn ---

    Câu hỏi: {query}

    Hãy phân tích tình huống và đưa ra câu trả lời dựa trên thông tin từ tin nhắn trên.
    Yêu cầu đối với câu trả lời:
    - Không sử dụng markdown, nhưng có thể sử dụng các kí hiệu.
    - Mỗi đoạn văn không quá 4096 ký tự.
    - Các gạch đầu dòng phải nối tiếp nhau, không có xuống dòng.
    """
)


class Prompt(containers.DeclarativeContainer):
    message = providers.Object(MESSAGE)
    conversation = providers.Object(CONVERSATION)
