from dependency_injector import containers, providers
from langchain_core.prompts import PromptTemplate

CONVERSATION = PromptTemplate.from_template(
    """
    Bạn là 1 người đang tổng hợp lại các tin nhắn được nhắn trong một nhóm trò chuyện giữa những người bạn.
    Dưới đây là một số cuộc hội thoại có liên quan đến câu hỏi. Mỗi cuộc hội thoại bắt đầu bằng <CONVERSATION> và kết thúc bằng </CONVERSATION>.

    --- Tin nhắn ---
    {context}
    --- Hết tin nhắn ---

    Câu hỏi: {query}

    Hãy phân tích tình huống và đưa ra câu trả lời kèm dẫn chứng.
    Yêu cầu đối với câu trả lời:
    - Không sử dụng markdown, nhưng có thể sử dụng các kí hiệu.
    - Mỗi đoạn văn không quá 4096 ký tự.
    - Các gạch đầu dòng phải nối tiếp nhau, không có xuống dòng.
    """
)

CONVERSATION2 = PromptTemplate.from_template(
    """
Bạn đang tổng hợp các tin nhắn từ một nhóm trò chuyện giữa những người bạn. Hãy phân tích các cuộc hội thoại dưới đây và trả lời câu hỏi một cách chi tiết, có dẫn chứng cụ thể.

--- TIN NHẮN ---
{context}
--- HẾT TIN NHẮN ---

Câu hỏi: {query}

Yêu cầu đối với câu trả lời:
- Không sử dụng định dạng markdown, nhưng có thể dùng các ký hiệu thông thường để làm nổi bật nội dung.
- Mỗi đoạn văn không vượt quá 4096 ký tự.
- Các gạch đầu dòng phải liên tiếp nhau không có dòng trống ở giữa.
- Đưa ra phân tích rõ ràng dựa trên bằng chứng từ các tin nhắn.
"""
)


class Prompt(containers.DeclarativeContainer):
    conversation = providers.Object(CONVERSATION)
    conversation2 = providers.Object(CONVERSATION2)
