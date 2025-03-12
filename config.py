from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache(1)
class Config(BaseSettings):
    model_config = SettingsConfigDict()

    google_api_key: str
    pinecone_api_key: str
    qdrant_url: str
    redis_url: str
    telegram_bot_token: str

    message_repository_key: str = "message"
    conversation_vectorstore_key: str = "conversation"
