import asyncio
from io import BytesIO

from discord.ext.commands import Context, command
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes, MessageHandler, filters

from app.core.chat_model import ChatModelService
from app.utils.image import ImageBytesToB64
from app.facial.facial_graph import FacialGraphService


class FacialHandler:
    def __init__(self, chat_model_service: ChatModelService):
        self.facial_graph_service = FacialGraphService(chat_model_service)

    @classmethod
    def syntax(cls):
        return ("facial", "Facial")

    def telegram_handler(self):
        async def handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
            if not update.message or not update.message.chat.id:
                return
            if not update.message.photo:
                await update.message.reply_text("Empty Query")
                return
            photo = update.message.photo[-1]

            file_ = await photo.get_file()
            image_bytes = await file_.download_as_bytearray()
            image_url = ImageBytesToB64().dump(image_bytes)

            await update.message.reply_chat_action(ChatAction.TYPING)
            for _, state in self.facial_graph_service.run(image_url):
                bot_messages = state.get("bot_messages", [])
                if not bot_messages:
                    continue
                await update.message.reply_chat_action(ChatAction.TYPING)
                bot_message = bot_messages[-1]
                await bot_message.reply_telegram(update)
                await asyncio.sleep(0.25)

        _filters = filters.PHOTO & filters.CaptionRegex(f"^/{self.syntax()[0]}")
        return MessageHandler(_filters, handler)

    def discord_handler(self):
        @command(name=self.syntax()[0], help=self.syntax()[1])
        async def handler(ctx: Context):
            attachments = ctx.message.attachments
            if not attachments:
                await ctx.send("Empty Query")
                return

            attachment = attachments[0]
            with BytesIO() as buffer:
                await attachment.save(buffer)
                image_url = ImageBytesToB64().dump(buffer.getvalue())

            await ctx.send("⏳ Đang luận giải...")
            for _, state in self.facial_graph_service.run(image_url):
                bot_messages = state.get("bot_messages", [])
                if not bot_messages:
                    continue

                bot_message = bot_messages[-1]
                await bot_message.reply_discord(ctx)
                await asyncio.sleep(0.25)

        return handler
