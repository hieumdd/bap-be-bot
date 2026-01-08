import pytest

from app.core.database import MongoDBService
from app.user.user_model import TelegramUser
from app.user.user_service import UserService


class TestUser:
    @pytest.fixture
    def user_service(self, mongodb_service: MongoDBService):
        return UserService(mongodb_service)

    @pytest.fixture
    def chat_id(self) -> int:
        return -859761464

    @pytest.fixture
    def user(self, chat_id: int) -> TelegramUser:
        return TelegramUser(id=852795805, chat_id=chat_id, full_name="HM")

    def test_upsert_user(self, user_service: UserService, user: TelegramUser):
        result = user_service.upsert_user(user)
        assert result

    def test_return_mention_all_message(self, user_service: UserService, chat_id: int):
        message = user_service.return_mention_all_message(chat_id)
        assert message
