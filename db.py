from qdrant_client import QdrantClient
import redis

from logger import get_logger
from config import config

logger = get_logger(__name__)

redis_client = redis.Redis.from_url(config.redis_url, decode_responses=True)
qdrant_client = QdrantClient(url=config.qdrant_url)
