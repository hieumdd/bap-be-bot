from functools import lru_cache

from langchain_pinecone import PineconeEmbeddings
from langchain_qdrant import QdrantVectorStore

from logger import get_logger
from config import Config
from db import qdrant_client

logger = get_logger(__name__)


@lru_cache(1)
def embedding(config=Config):
    logger.debug("Initialized Embedding")
    return PineconeEmbeddings(
        model="multilingual-e5-large",
        pinecone_api_key=config().pinecone_api_key,
    )


@lru_cache(1)
def vectorstore(config=Config, embedding=embedding):
    logger.debug("Initialized VectorStore")
    return QdrantVectorStore(
        client=qdrant_client(),
        embedding=embedding(),
        collection_name=config().conversation_vectorstore_key,
    )
