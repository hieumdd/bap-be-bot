from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    google_api_key: str

    telegram_bot_token: str
    discord_bot_token: str
