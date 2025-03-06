import os

import chromadb
from qdrant_client import QdrantClient
import redis

CHROMA_CLIENT = chromadb.PersistentClient("./.chroma")
QDRANT_CLIENT = QdrantClient(url=os.getenv("QDRANT_URL"))
REDIS_CLIENT = redis.Redis.from_url(os.getenv("REDIS_URL"))
