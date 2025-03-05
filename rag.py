import os

import chromadb
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold
from langchain_huggingface import HuggingFaceEmbeddings

from logger import get_logger

logger = get_logger(__name__)

CHROMA_CLIENT = chromadb.PersistentClient("./.chroma")
EMBEDDING_VIETNAMESE = HuggingFaceEmbeddings(
    model_name="dangvantuan/vietnamese-embedding"
)
LLM = GoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY: HarmBlockThreshold.BLOCK_NONE,
    },
)

PROMPT1 = PromptTemplate.from_template(
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

PROMPT2 = PromptTemplate.from_template(
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


class RAG:
    def __init__(self, llm=LLM):
        self.vector_store = RAG.create_vector_store("telegram")
        self.llm = llm

    @staticmethod
    def create_vector_store(collection_name: str, embeddings=EMBEDDING_VIETNAMESE):
        return Chroma(
            client=CHROMA_CLIENT,
            embedding_function=embeddings,
            collection_name=collection_name,
            collection_metadata={"hnsw:space": "cosine"},
        )

    async def search(self, query: str, k=15):
        documents = await self.vector_store.asimilarity_search(query, k)
        return map(lambda d: d.page_content, documents)

    async def answer(self, query: str, prompt: PromptTemplate = PROMPT2):
        results = await self.search(query)
        conversations = map(
            lambda c: f"""
            <CONVERSATION>
            {c}
            </CONVERSATION>
            """,
            results,
        )
        context = "\n".join(conversations)
        response = (prompt | self.llm).invoke({"query": query, "context": context})
        return response
