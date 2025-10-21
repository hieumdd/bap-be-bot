from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from app.core.logger import get_logger
from app.core.settings import Settings
from app.core.chat_model import ChatModelService
from app.tarot.tarot_handler import TAROT_COMMAND, TAROT_DESCRIPTION, TarotHandler
from app.ziwei.ziwei_handler import ZIWEI_COMMAND, ZIWEI_DESCRIPTION, ZiweiHandler


logger = get_logger(__name__)


async def post_init(application: Application):
    commands = [
        (TAROT_COMMAND, TAROT_DESCRIPTION),
        (ZIWEI_COMMAND, ZIWEI_DESCRIPTION),
    ]
    await application.bot.set_my_commands(commands)
    logger.debug("Telegram Bot is running")


async def on_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error = context.error
    logger.error(error)
    await update.message.reply_text("Unknown Error Ocurred")


if __name__ == "__main__":
    settings = Settings()

    token = settings.telegram_bot_token
    application = Application.builder().token(token).post_init(post_init).build()

    chat_model_service = ChatModelService(settings=settings)

    application.add_handler(CommandHandler(TAROT_COMMAND, TarotHandler(chat_model_service).telegram_handler))
    application.add_handler(CommandHandler(ZIWEI_COMMAND, ZiweiHandler(chat_model_service).telegram_handler))
    application.add_error_handler(on_error)

    application.run_polling()
