from dataclasses import dataclass

from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.language_models.llms import BaseLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.retrievers import BaseRetriever

from logger import get_logger

logger = get_logger(__name__)


@dataclass
class RAG:
    retriever: BaseRetriever
    llm: BaseLLM
    prompt: PromptTemplate

    async def answer(self, query: str):
        def format_docs(docs: list[Document]):
            conversations = map(lambda c: f"""<CONVERSATION>{c}</CONVERSATION>""", docs)
            return "\n".join(conversations)

        chain = (
            {"context": self.retriever | format_docs, "query": RunnablePassthrough()}
            | self.prompt
            | self.llm
        )
        response = await chain.ainvoke(query)
        return response
