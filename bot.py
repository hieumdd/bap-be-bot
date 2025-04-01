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
from app.core.config import config
from app.rag.message_model import Message
from app.rag.message_repository import message_repository
from app.rag.rag_graph import run_rag_graph
from app.ziwei.ziwei_graph import run_ziwei_graph


logger = get_logger(__name__)


async def post_init(application: Application):
    commands = [("query", "Query"), ("ziwei", "Ziwei Doushu")]
    await application.bot.set_my_commands(commands)
    logger.debug("Bot is running")


async def queue_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    message_repository.write(message)


async def rag_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.chat.id:
        return
    if not context.args:
        await update.message.reply_text("Empty Query")
        return

    await update.message.reply_chat_action(ChatAction.TYPING)
    question = " ".join(context.args)

    for _, state in run_rag_graph(question):
        for message in state["messages"][1:]:
            async for attempt in AsyncRetrying(
                wait=wait_fixed(2),
                stop=4,
                reraise=True,
            ):
                with attempt:
                    await update.message.reply_chat_action(ChatAction.TYPING)
                    await update.message.reply_text(
                        message.content[:4096],
                        parse_mode=ParseMode.HTML,
                    )
            await asyncio.sleep(0.25)


async def ziwei_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.chat.id:
        return
    if not context.args:
        await update.message.reply_text("Empty Query")
        return

    await update.message.reply_chat_action(ChatAction.TYPING)
    question = " ".join(context.args)

    for node_id, state in run_ziwei_graph(question):
        async for attempt in AsyncRetrying(wait=wait_fixed(2), stop=4, reraise=True):
            with attempt:
                await update.message.reply_chat_action(ChatAction.TYPING)
                if node_id == "generate_image":
                    await update.message.reply_photo(
                        state["birthchart_image"],
                        caption="Lá số Tử Vi",
                        parse_mode=ParseMode.HTML,
                    )
                if node_id == "write_analysis_file":
                    await update.message.reply_document(
                        state["analysis_file"],
                        filename="analysis.txt",
                        caption="Luận giải chi tiết",
                    )
                if node_id == "combine_summaries":
                    for summary in state["summaries"]:
                        await update.message.reply_text(
                            summary[:4096],
                            parse_mode=ParseMode.HTML,
                        )
                if node_id == "handle_error":
                    await update.message.reply_text(
                        state["messages"][-1].content[:4096],
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
    application.add_handler(MessageHandler(text_message, queue_message))
    application.add_handler(CommandHandler("query", rag_answer))
    application.add_handler(CommandHandler("ziwei", ziwei_answer))
    application.add_error_handler(on_error)

    application.run_polling()
