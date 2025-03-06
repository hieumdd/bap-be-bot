from abc import ABC, abstractmethod
from typing import Any

from dependency_injector import containers, providers
from langchain_core.vectorstores import VectorStore
from langchain_chroma.vectorstores import Chroma
from langchain_qdrant import QdrantVectorStore as Qdrant

from logger import get_logger

logger = get_logger(__name__)


class CustomVectorStore(ABC, VectorStore):
    @abstractmethod
    def id_encoder(self, id):
        pass

    async def upsert(self, rows: list[dict[str, Any]]):
        await self.aadd_texts(
            texts=[x["texts"] for x in rows],
            ids=[self.id_encoder(x["conversation_id"]) for x in rows],
            metadatas=rows,
        )


class ChromaVectorStore(Chroma, CustomVectorStore):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, collection_metadata={"hnsw:space": "cosine"})

    def id_encoder(self, id: Any):
        return str(id)


class QdrantVectorStore(Qdrant, CustomVectorStore):
    def id_encoder(self, id: Any):
        return int(id)


class VectorStore(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.DependenciesContainer()
    embedding = providers.Dependency()

    chroma = providers.Singleton(
        ChromaVectorStore,
        client=db.chroma,
        embedding_function=embedding,
        collection_name=config.vectorstore_key,
    )
    qdrant = providers.Singleton(
        QdrantVectorStore,
        client=db.qdrant,
        embedding=embedding,
        collection_name=config.vectorstore_key,
    )
    vectorstore = providers.Selector(config.vectorstore, chroma=chroma, qdrant=qdrant)
