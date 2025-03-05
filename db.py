import os

import chromadb
import redis

CHROMA_CLIENT = chromadb.PersistentClient("./.chroma")
REDIS_CLIENT = redis.Redis.from_url(os.getenv("REDIS_URL"))
