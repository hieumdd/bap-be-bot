import discord
from discord.ext import commands

from app.core.logger import get_logger
from app.core.settings import Settings
from app.core.chat_model import ChatModelService
from app.tarot.tarot_handler import TAROT_COMMAND, TarotHandler
from app.ziwei.ziwei_handler import ZIWEI_COMMAND, ZiweiHandler

logger = get_logger(__name__)

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logger.debug("Discord Bot is running")


@bot.command(name=TAROT_COMMAND)
async def tarot_command(ctx, *, question: str = None):
    await tarot_handler.discord_handler(ctx, question)


@bot.command(name=ZIWEI_COMMAND)
async def ziwei_command(ctx, *, question: str = None):
    await ziwei_handler.discord_handler(ctx, question)


@bot.event
async def on_command_error(ctx, error):
    logger.error(error)
    await ctx.send("Unknown Error Ocurred")


if __name__ == "__main__":
    settings = Settings()

    chat_model_service = ChatModelService(settings=settings)
    tarot_handler = TarotHandler(chat_model_service)
    ziwei_handler = ZiweiHandler(chat_model_service)

    bot.run(settings.discord_bot_token)
