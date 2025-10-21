import asyncio

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from app.core.chat_model import ChatModelService
from app.ziwei.ziwei_graph import ZiweiGraphService

ZIWEI_COMMAND = "ziwei"
ZIWEI_DESCRIPTION = "Ziwei"


class ZiweiHandler:
    def __init__(self, chat_model_service: ChatModelService):
        self.ziwei_graph_service = ZiweiGraphService(chat_model_service)

    async def telegram_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.chat.id:
            return
        if not context.args:
            await update.message.reply_text("Empty Query")
            return

        await update.message.reply_chat_action(ChatAction.TYPING)
        question = " ".join(context.args)
        for _, state in self.ziwei_graph_service.run(question):
            bot_messages = state.get("bot_messages", [])
            if not bot_messages:
                continue
            await update.message.reply_chat_action(ChatAction.TYPING)
            bot_message = bot_messages[-1]
            await bot_message.reply_telegram(update)
            await asyncio.sleep(0.25)
