from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import os

from langchain_core.prompts import PromptTemplate
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore as LVectorStore
from langchain_chroma.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore as Qdrant

from logger import get_logger
from db import CHROMA_CLIENT, QDRANT_CLIENT

logger = get_logger(__name__)

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


@dataclass
class VectorStore(ABC):
    key_name: str
    embeddings: Embeddings = field(default_factory=lambda: EMBEDDING_VIETNAMESE)
    vector_store: LVectorStore = field(init=False)

    @abstractmethod
    def id_encoder(self, id):
        pass

    async def upsert(self, rows):
        await self.vector_store.aadd_texts(
            texts=[x["texts"] for x in rows],
            ids=[self.id_encoder(x["conversation_id"]) for x in rows],
            metadatas=rows,
        )


class ChromaVectorStore(VectorStore):
    def __post_init__(self):
        self.vector_store = Chroma(
            client=CHROMA_CLIENT,
            embedding_function=self.embeddings,
            collection_name=self.key_name,
            collection_metadata={"hnsw:space": "cosine"},
        )

    def id_encoder(self, id):
        return str(id)


class QdrantVectorStore(VectorStore):
    def __post_init__(self):
        self.vector_store = Qdrant(
            client=QDRANT_CLIENT,
            embedding=self.embeddings,
            collection_name=self.key_name,
        )

    def id_encoder(self, id):
        return int(id)


class RAG:
    def __init__(self, embeddings: Embeddings = EMBEDDING_VIETNAMESE, llm=LLM):
        self.vector_store = QdrantVectorStore("telegram", embeddings)
        self.llm = llm

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
