from langchain_pinecone import PineconeEmbeddings
from langchain_qdrant import QdrantVectorStore

from config import CONFIG
from db import QDRANT_CLIENT

EMBEDDING = PineconeEmbeddings(
    model="multilingual-e5-large",
    pinecone_api_key=CONFIG.pinecone_api_key,
)

VECTORSTORE = QdrantVectorStore(
    client=QDRANT_CLIENT,
    embedding=EMBEDDING,
    collection_name=CONFIG.conversation_vectorstore_key,
)
