from qdrant_client import QdrantClient
import redis

from app.core.settings import config

redis_client = redis.Redis.from_url(config.redis_url, decode_responses=True)
qdrant_client = QdrantClient(url=config.qdrant_url)
