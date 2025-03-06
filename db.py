import chromadb
from dependency_injector import containers, providers
from qdrant_client import QdrantClient
import redis


class DB(containers.DeclarativeContainer):
    config = providers.Configuration()

    chroma = providers.Singleton(chromadb.PersistentClient, path="./.chroma")
    qdrant = providers.Singleton(QdrantClient, url=config.qdrant_url)
    redis = providers.Singleton(redis.Redis.from_url, url=config.redis_url)
