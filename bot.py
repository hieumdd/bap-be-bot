import asyncio
import json

from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from tenacity import AsyncRetrying, Retrying, wait_fixed

from logger import get_logger
from config import Config
from db import redis_client
import rag


logger = get_logger(__name__)


def build_application(config=Config):
    async def post_init(application: Application):
        await application.bot.set_my_commands([("query", "Query")])
        logger.debug("Bot is running")

    token = config().telegram_bot_token
    return Application.builder().token(token).post_init(post_init).build()


def queue_message(redis=redis_client):
    async def _queue_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.chat.id:
            return
        message = update.message
        row = {
            "chat_id": str(abs(update.message.chat.id)),
            "id": message.id,
            "from": message.from_user.full_name,
            "text": message.text,
            "timestamp": int(message.date.timestamp()),
        }
        logger.debug(f"Push to Redis: {row}")
        for attempt in Retrying(wait=wait_fixed(2)):
            with attempt:
                redis().rpush("message", json.dumps(row))

    return _queue_message


def answer(rag=rag.answer):
    async def _answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.chat.id:
            return
        if not context.args:
            await update.message.reply_text("Empty Query")
            return
        await update.message.reply_chat_action(ChatAction.TYPING)
        query = " ".join(context.args)
        response = await rag(query)
        for text in response.split("\n\n"):
            async for attempt in AsyncRetrying(wait=wait_fixed(2)):
                with attempt:
                    await update.message.reply_chat_action(ChatAction.TYPING)
                    await update.message.reply_text(
                        text[:4096], parse_mode=ParseMode.HTML
                    )
                    await asyncio.sleep(0.25)

    return _answer


async def on_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error = context.error
    logger.error(error)


if __name__ == "__main__":
    application = build_application()

    text_message = filters.TEXT & ~filters.COMMAND
    application.add_handler(MessageHandler(text_message, queue_message()))
    application.add_handler(CommandHandler("query", answer()))
    application.add_error_handler(on_error)

    application.run_polling()
