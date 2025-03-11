from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    qdrant_url: str
    redis_url: str
    google_api_key: str
    pinecone_api_key: str
    telegram_bot_token: str

    message_repository_key: str = "message"
    conversation_vectorstore_key: str = "conversation"


CONFIG = Settings()
