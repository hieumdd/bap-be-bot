from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

from app.core.settings import config
from app.core.db import qdrant_client

embedding = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")

vectorstore = QdrantVectorStore(
    client=qdrant_client,
    embedding=embedding,
    collection_name=config.conversation_vectorstore_key,
)
