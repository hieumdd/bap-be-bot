from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from app.core.chat_model import ChatModelService
from app.tarot.tarot_handler import TarotHandler
from logger import get_logger
from app.core.settings import Settings


logger = get_logger(__name__)


async def post_init(application: Application):
    commands = [
        ("tarot", "Tarot"),
    ]
    await application.bot.set_my_commands(commands)
    logger.debug("Bot is running")


async def on_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error = context.error
    logger.error(error)


if __name__ == "__main__":
    settings = Settings()

    token = settings.telegram_bot_token
    application = Application.builder().token(token).post_init(post_init).build()

    chat_model_service = ChatModelService(settings=settings)

    application.add_handler(CommandHandler("tarot", TarotHandler(chat_model_service).telegram_handler))
    application.add_error_handler(on_error)

    application.run_polling()
