import asyncio

from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from tenacity import AsyncRetrying, wait_fixed

from logger import get_logger
from config import config
from models.message import Message, MessageRepository
import rag


logger = get_logger(__name__)


async def post_init(application: Application):
    await application.bot.set_my_commands([("query", "Query")])
    logger.debug("Bot is running")


def queue_message():
    repository = MessageRepository()

    async def _queue_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.chat.id:
            return
        message = Message(
            chat_id=abs(update.message.chat.id),
            id=update.message.id,
            timestamp=int(update.message.date.timestamp()),
            from_=update.message.from_user.full_name,
            text=update.message.text,
        )
        logger.debug(f"Push to Redis: {message}")
        repository.write(message)

    return _queue_message


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.chat.id:
        return
    if not context.args:
        await update.message.reply_text("Empty Query")
        return
    await update.message.reply_chat_action(ChatAction.TYPING)
    query = " ".join(context.args)
    response = await rag.answer(query)
    for text in response.split("\n\n"):
        async for attempt in AsyncRetrying(wait=wait_fixed(2), stop=4, reraise=True):
            with attempt:
                await update.message.reply_chat_action(ChatAction.TYPING)
                await update.message.reply_text(
                    text[:4096],
                    parse_mode=ParseMode.HTML,
                )
                await asyncio.sleep(0.25)


async def on_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error = context.error
    logger.error(error)


if __name__ == "__main__":
    token = config.telegram_bot_token
    application = Application.builder().token(token).post_init(post_init).build()

    text_message = filters.TEXT & ~filters.COMMAND
    application.add_handler(MessageHandler(text_message, queue_message()))
    application.add_handler(CommandHandler("query", answer))
    application.add_error_handler(on_error)

    application.run_polling()
