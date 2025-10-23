import asyncio
import base64

from discord.ext.commands import Context
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes, filters

from app.core.chat_model import ChatModelService
from app.facial.facial_graph import FacialGraphService

FACIAL_COMMAND = "facial"
FACIAL_TELEGRAM_FILTER = filters.PHOTO & filters.CaptionRegex(f"^/{FACIAL_COMMAND}")
FACIAL_DESCRIPTION = "Facial"


class FacialHandler:
    def __init__(self, chat_model_service: ChatModelService):
        self.facial_graph_service = FacialGraphService(chat_model_service)

    async def telegram_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.chat.id:
            return
        if not update.message.photo:
            await update.message.reply_text("Empty Query")
            return
        photo = update.message.photo[-1]

        file_ = await photo.get_file()
        image_bytes = await file_.download_as_bytearray()
        image_url = f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode()}"
        print(image_url)

        await update.message.reply_chat_action(ChatAction.TYPING)
        for _, state in self.facial_graph_service.run(image_url):
            bot_messages = state.get("bot_messages", [])
            if not bot_messages:
                continue
            await update.message.reply_chat_action(ChatAction.TYPING)
            bot_message = bot_messages[-1]
            await bot_message.reply_telegram(update)
            await asyncio.sleep(0.25)

    async def discord_handler(self, ctx: Context, question: str):
        if not question:
            await ctx.reply("Empty Query")
            return

        await ctx.reply("⏳ Đang luận giải...")

        for _, state in self.facial_graph_service.run(question):
            bot_messages = state.get("bot_messages", [])
            if not bot_messages:
                continue

            bot_message = bot_messages[-1]
            await bot_message.reply_discord(ctx)
            await asyncio.sleep(0.25)
