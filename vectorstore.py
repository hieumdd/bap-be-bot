from abc import ABC, abstractmethod
from typing import Any

from dependency_injector import containers, providers
from langchain_core.vectorstores import VectorStore
from langchain_qdrant import QdrantVectorStore as Qdrant

from logger import get_logger

logger = get_logger(__name__)


class CustomVectorStore(VectorStore, ABC):
    @abstractmethod
    def id_encoder(self, id):
        pass

    async def upsert(self, rows: list[dict[str, Any]]):
        await self.aadd_texts(
            texts=[x["texts"] for x in rows],
            ids=[self.id_encoder(x["conversation_id"]) for x in rows],
            metadatas=rows,
        )


class QdrantVectorStore(Qdrant, CustomVectorStore):
    def id_encoder(self, id: Any):
        return int(id)


def as_retriever(vs: VectorStore, k: int):
    return vs.as_retriever(search_type="similarity", search_kwargs={"k": k})


class VectorStore(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.DependenciesContainer()
    embedding = providers.Dependency()

    qdrant = providers.Singleton(
        QdrantVectorStore,
        client=db.qdrant,
        embedding=embedding,
        collection_name=config.vectorstore_key,
    )
    vectorstore = providers.Selector(config.vectorstore, qdrant=qdrant)
    retriever = providers.Factory(as_retriever, vs=vectorstore, k=config.retriever_k)
