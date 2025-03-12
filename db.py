from functools import lru_cache

from qdrant_client import QdrantClient
import redis

from logger import get_logger
from config import Config

logger = get_logger(__name__)


@lru_cache(1)
def redis_client(config=Config):
    logger.debug("Initialized Redis")
    return redis.Redis.from_url(config().redis_url, decode_responses=True)


@lru_cache(1)
def qdrant_client(config=Config):
    logger.debug("Initialized Qdrant")
    return QdrantClient(url=config().qdrant_url)
