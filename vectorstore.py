from langchain_pinecone import PineconeEmbeddings
from langchain_qdrant import QdrantVectorStore

from config import config
from db import qdrant_client

embedding = PineconeEmbeddings(
    model="multilingual-e5-large",
    pinecone_api_key=config.pinecone_api_key,
)

vectorstore = QdrantVectorStore(
    client=qdrant_client,
    embedding=embedding,
    collection_name=config.conversation_vectorstore_key,
)
