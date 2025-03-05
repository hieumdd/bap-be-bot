import asyncio
import json
import os

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from logger import get_logger
from db import REDIS_CLIENT
from rag import RAG


logger = get_logger(__name__)


async def queue_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    REDIS_CLIENT.rpush("message", json.dumps(row))


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.chat.id:
        return
    if not context.args:
        await update.message.reply_text("Empty Query")
    await update.message.reply_chat_action(ChatAction.TYPING)
    query = " ".join(context.args)
    embeddings = RAG()
    response = await embeddings.answer(query)
    for text in response.split("\n\n"):
        await update.message.reply_chat_action(ChatAction.TYPING)
        await asyncio.sleep(0.25)
        await update.message.reply_text(text[:4096])


if __name__ == "__main__":
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    text_message = filters.TEXT & ~filters.COMMAND
    application.add_handler(MessageHandler(text_message, queue_message))
    application.add_handler(CommandHandler("query", answer))

    logger.debug("Bot is running")
    application.run_polling()
