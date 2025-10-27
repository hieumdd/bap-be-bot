from discord.ext.commands import Context, command
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from app.donate.donate_service import DonateService


class DonateHandler:
    def __init__(self):
        self.donate_service = DonateService()

    @classmethod
    def syntax(cls):
        return ("donate", "Donate")

    def telegram_handler(self):
        async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            message = self.donate_service.return_donation_message()
            await message.reply_telegram(update)

        return CommandHandler(self.syntax()[0], handler)

    def discord_handler(self):
        @command(name=self.syntax()[0], help=self.syntax()[1])
        async def handler(ctx: Context, *args):
            message = self.donate_service.return_donation_message()
            await message.reply_discord(ctx)

        return handler
