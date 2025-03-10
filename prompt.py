from dependency_injector import containers, providers
from langchain_core.prompts import PromptTemplate

CONVERSATION = PromptTemplate.from_template(
    """
    Bạn đang tổng hợp các tin nhắn từ một nhóm trò chuyện giữa những người bạn. Hãy phân tích các cuộc hội thoại dưới đây và trả lời câu hỏi một cách chi tiết, có dẫn chứng cụ thể.

    --- TIN NHẮN ---
    {context}
    --- HẾT TIN NHẮN ---

    Câu hỏi: {query}

    Yêu cầu đối với câu trả lời:
    - Mỗi đoạn văn không vượt quá 4096 ký tự.
    - Các gạch đầu dòng phải liên tiếp nhau không có dòng trống ở giữa.
    - Đưa ra phân tích rõ ràng dựa trên bằng chứng từ các tin nhắn.
    - Each section should be formatted using **HTML** tags as per Telegram's [formatting options](https://core.telegram.org/bots/api#formatting-options).
    - Use ONLY the following tags:
        - `<b>` for **bold text**
        - `<i>` for *italic text*
        - `<u>` for __underlined text__
        - `<s>` for ~~strikethrough text~~
        - `<code>` for inline `monospace`
        - `<pre>` for code blocks (use `<pre><code class="language">...</code></pre>` for syntax highlighting)
        - `<a href="URL">` for hyperlinks
        - `<blockquote>` for block quotes
    """
)


class Prompt(containers.DeclarativeContainer):
    conversation = providers.Object(CONVERSATION)
