from dataclasses import dataclass

from langchain_core.prompts import PromptTemplate
from langchain_core.language_models.llms import BaseLLM
from langchain_core.vectorstores import VectorStore

from logger import get_logger

logger = get_logger(__name__)


@dataclass
class RAG:
    vectorstore: VectorStore
    llm: BaseLLM
    prompt: PromptTemplate

    async def search(self, query: str, k=10):
        documents = await self.vectorstore.asimilarity_search(query, k)
        return map(lambda d: d.page_content, documents)

    async def answer(self, query: str):
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
        response = (self.prompt | self.llm).invoke({"query": query, "context": context})
        return response
