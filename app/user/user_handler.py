from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from app.core.database import MongoDBService
from app.user.user_model import TelegramUser
from app.user.user_service import UserService


class UserHandler:
    def __init__(self, mongodb_service: MongoDBService):
        self.user_service = UserService(mongodb_service)

    @classmethod
    def syntax(cls):
        return ("all", "@all")

    def message_handler(self):
        async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = TelegramUser.from_update(update)
            self.user_service.upsert_user(user)

        return MessageHandler(filters.TEXT & ~filters.COMMAND, handler)

    def command_handler(self):
        async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            message = self.user_service.return_mention_all_message(update.effective_chat.id)
            await message.reply_telegram(update)

        return CommandHandler(self.syntax()[0], handler)
