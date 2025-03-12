from functools import lru_cache
import re

from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold

from config import Config
from vectorstore import vectorstore


@lru_cache(1)
def llm(config=Config):
    return GoogleGenerativeAI(
        model="gemini-2.0-flash",
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY: HarmBlockThreshold.BLOCK_NONE,
        },
        google_api_key=config().google_api_key,
    )


@lru_cache(1)
def prompt():
    return PromptTemplate.from_template(
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
        """
    )


async def answer(query: str, k=10, vectorstore=vectorstore, prompt=prompt, llm=llm):
    def format_docs(docs: list[Document]):
        conversations = map(
            lambda c: f"<CONVERSATION>\n{c.page_content}\n</CONVERSATION>",
            docs,
        )
        return "\n".join(conversations)

    def format_html(text: str):
        text = re.sub(r"\*\*(.*?)\*\*|__(.*?)__", r"<b>\1\2</b>", text)
        text = re.sub(r"\*(.*?)\*|_(.*?)_", r"<i>\1\2</i>", text)
        return text

    retriever = vectorstore().as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
    chain = (
        {"context": retriever | format_docs, "query": RunnablePassthrough()}
        | prompt()
        | llm()
        | format_html
    )
    response = await chain.ainvoke(query)
    return response
