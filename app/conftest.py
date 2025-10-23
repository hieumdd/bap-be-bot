import pytest

from app.core.chat_model import ChatModelService


@pytest.fixture
def chat_model_service():
    return ChatModelService()
