import pytest

from app.core.database import MongoDBService
from app.core.settings import Settings
from app.core.chat_model import ChatModelService


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture
def chat_model_service(settings: Settings):
    return ChatModelService(settings)


@pytest.fixture
def mongodb_service(settings: Settings):
    with MongoDBService(settings) as mongodb_service:
        yield mongodb_service
