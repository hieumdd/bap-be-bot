from functools import lru_cache

from langchain_pinecone import PineconeEmbeddings
from langchain_qdrant import QdrantVectorStore

from config import Config
from db import qdrant_client


@lru_cache(1)
def embedding(config=Config):
    return PineconeEmbeddings(
        model="multilingual-e5-large",
        pinecone_api_key=config().pinecone_api_key,
    )


@lru_cache(1)
def vectorstore(config=Config, embedding=embedding):
    return QdrantVectorStore(
        client=qdrant_client(),
        embedding=embedding(),
        collection_name=config().conversation_vectorstore_key,
    )
