import asyncio
import json

from dependency_injector.wiring import Provide, inject
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from tenacity import AsyncRetrying, Retrying, wait_fixed

from logger import get_logger
from container import Container
from rag import RAG


logger = get_logger(__name__)


@inject
def build_application(token: str = Provide[Container.config.telegram_bot_token]):
    async def post_init(application: Application):
        await application.bot.set_my_commands([("query", "Query")])
        logger.debug("Bot is running")

    application = Application.builder().token(token).post_init(post_init).build()
    return application


@inject
async def queue_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    redis=Provide[Container.db.redis],
):
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
            redis.rpush("message", json.dumps(row))


@inject
async def answer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    rag: RAG = Provide[Container.rag],
):
    if not update.message or not update.message.chat.id:
        return
    if not context.args:
        await update.message.reply_text("Empty Query")
        return
    await update.message.reply_chat_action(ChatAction.TYPING)
    query = " ".join(context.args)
    response = await rag.answer(query)
    for text in response.split("\n\n"):
        async for attempt in AsyncRetrying(wait=wait_fixed(2)):
            with attempt:
                await update.message.reply_chat_action(ChatAction.TYPING)
                await asyncio.sleep(0.25)
                await update.message.reply_text(text[:4096])


async def on_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error = context.error
    logger.error(error)


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    application = build_application()

    text_message = filters.TEXT & ~filters.COMMAND
    application.add_handler(MessageHandler(text_message, queue_message))
    application.add_handler(CommandHandler("query", answer))
    application.add_error_handler(on_error)

    application.run_polling()
