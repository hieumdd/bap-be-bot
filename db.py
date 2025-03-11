from qdrant_client import QdrantClient
import redis

from logger import get_logger
from config import CONFIG

logger = get_logger(__name__)

REDIS_CLIENT = redis.Redis.from_url(CONFIG.redis_url)

QDRANT_CLIENT = QdrantClient(url=CONFIG.qdrant_url)
