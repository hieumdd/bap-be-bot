from app.core.config import config
from app.core.db import qdrant_client

from logger import get_logger

logger = get_logger(__name__)


def migrate():
    collection_name = config.conversation_vectorstore_key
    if qdrant_client.collection_exists(collection_name):
        logger.info(f"Collection {collection_name} already exists")
        return
    qdrant_client.create_collection(
        config.conversation_vectorstore_key,
        vectors_config={"size": 384, "distance": "Cosine"},
        hnsw_config={
            "m": 16,
            "ef_construct": 100,
            "full_scan_threshold": 10000,
            "max_indexing_threads": 0,
            "on_disk": True,
        },
    )
    logger.info(f"Created Collection {collection_name}")


if __name__ == "__main__":
    migrate()
