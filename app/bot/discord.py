import discord
from discord.ext import commands

from app.core.logger import get_logger
from app.core.settings import Settings
from app.core.chat_model import ChatModelService
from app.facial.facial_handler import FacialHandler
from app.tarot.tarot_handler import TarotHandler
from app.ziwei.ziwei_handler import ZiweiHandler

logger = get_logger(__name__)

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logger.debug("Discord Bot is running")


@bot.event
async def on_command_error(ctx, error):
    logger.error(error)
    await ctx.send("Unknown Error Ocurred")


if __name__ == "__main__":
    settings = Settings()

    chat_model_service = ChatModelService(settings=settings)

    bot.add_command(FacialHandler(chat_model_service).discord_handler())
    bot.add_command(TarotHandler(chat_model_service).discord_handler())
    bot.add_command(ZiweiHandler(chat_model_service).discord_handler())

    bot.run(settings.discord_bot_token, log_handler=None)
