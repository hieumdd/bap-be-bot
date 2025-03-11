from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold

from config import CONFIG
from vectorstore import VECTORSTORE

LLM = GoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY: HarmBlockThreshold.BLOCK_NONE,
    },
    google_api_key=CONFIG.google_api_key,
)


PROMPT = PromptTemplate.from_template(
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


async def answer(query: str, k=10):
    def format_docs(docs: list[Document]):
        conversations = map(lambda c: f"""<CONVERSATION>{c}</CONVERSATION>""", docs)
        return "\n".join(conversations)

    retriever = VECTORSTORE.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
    chain = (
        {"context": retriever | format_docs, "query": RunnablePassthrough()}
        | PROMPT
        | LLM
    )
    response = await chain.ainvoke(query)
    return response
