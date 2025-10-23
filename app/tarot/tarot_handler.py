import asyncio

from discord.ext.commands import Context, command
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import CommandHandler, ContextTypes

from app.core.chat_model import ChatModelService
from app.tarot.tarot_graph import TarotGraphService


class TarotHandler:
    def __init__(self, chat_model_service: ChatModelService):
        self.tarot_graph_service = TarotGraphService(chat_model_service)

    @classmethod
    def syntax(cls):
        return ("tarot", "Tarot")

    def telegram_handler(self):
        async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if not update.message or not update.message.chat.id:
                return
            if not context.args:
                await update.message.reply_text("Empty Query")
                return

            await update.message.reply_chat_action(ChatAction.TYPING)
            question = " ".join(context.args)
            for _, state in self.tarot_graph_service.run(question):
                bot_messages = state.get("bot_messages", [])
                if not bot_messages:
                    continue
                await update.message.reply_chat_action(ChatAction.TYPING)
                bot_message = bot_messages[-1]
                await bot_message.reply_telegram(update)
                await asyncio.sleep(0.25)

        return CommandHandler(self.syntax()[0], handler)

    def discord_handler(self):
        @command(name=self.syntax()[0], help=self.syntax()[1])
        async def handler(ctx: Context, *, question: str):
            if not question:
                await ctx.send("Empty Query")
                return

            await ctx.send("⏳ Đang luận giải...")

            for _, state in self.tarot_graph_service.run(question):
                bot_messages = state.get("bot_messages", [])
                if not bot_messages:
                    continue

                bot_message = bot_messages[-1]
                await bot_message.reply_discord(ctx)
                await asyncio.sleep(0.25)

        return handler
