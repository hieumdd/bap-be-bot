import pymongo
import pymongo.collection

from app.bot.message import TextMessage
from app.core.database import MongoDBService
from app.user.user_model import TelegramUser


class UserService:
    def __init__(self, mongodb_service: MongoDBService):
        self.client = mongodb_service.client

    @property
    def collection(self) -> pymongo.collection.Collection:
        return self.client["bap-be-bot"]["telegram-users"]

    def upsert_user(self, user: TelegramUser):
        return self.collection.update_one({"_id": user._id}, {"$set": user.model_dump()}, upsert=True)

    def return_mention_all_message(self, chat_id: int):
        cursor = self.collection.find({"_id.chat_id": chat_id}).sort("first_name", pymongo.ASCENDING)
        users = [TelegramUser.model_validate(user) for user in cursor]
        message_content = [f'<a href="tg://user?id={user.id}">{user.full_name}</a>' for user in users]
        message = TextMessage("\n".join(message_content))
        return message
