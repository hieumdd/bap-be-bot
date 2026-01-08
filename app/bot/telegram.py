from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, Defaults, ContextTypes

from app.core.database import MongoDBService
from app.core.logger import get_logger
from app.core.settings import Settings
from app.core.chat_model import ChatModelService
from app.donate.donate_handler import DonateHandler
from app.facial.facial_handler import FacialHandler
from app.tarot.tarot_handler import TarotHandler
from app.user.user_handler import UserHandler
from app.ziwei.ziwei_handler import ZiweiHandler


logger = get_logger(__name__)


async def post_init(application: Application):
    commands = [
        DonateHandler.syntax(),
        FacialHandler.syntax(),
        TarotHandler.syntax(),
        UserHandler.syntax(),
        ZiweiHandler.syntax(),
    ]
    await application.bot.set_my_commands(commands)
    logger.debug("Telegram Bot is running")


async def on_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(context.error)
    await update.message.reply_text("Unknown Error Ocurred")


if __name__ == "__main__":
    settings = Settings()
    chat_model_service = ChatModelService(settings=settings)

    token = settings.telegram_bot_token
    defaults = Defaults(parse_mode=ParseMode.HTML, allow_sending_without_reply=True)
    application = Application.builder().token(token).defaults(defaults).post_init(post_init).build()

    with MongoDBService(settings) as mongodb_service:
        user_handler = UserHandler(mongodb_service)

        application.add_handler(DonateHandler().telegram_handler())
        application.add_handler(FacialHandler(chat_model_service).telegram_handler())
        application.add_handler(TarotHandler(chat_model_service).telegram_handler())
        application.add_handler(user_handler.message_handler())
        application.add_handler(user_handler.command_handler())
        application.add_handler(ZiweiHandler(chat_model_service).telegram_handler())
        application.add_error_handler(on_error)

        application.run_polling()
