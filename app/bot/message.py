from dataclasses import dataclass
from io import BytesIO
from typing import Protocol, runtime_checkable

import discord
from discord.ext.commands.context import Context
from telegram import InputMediaPhoto, Update
from tenacity import retry, stop_after_attempt, wait_fixed


def with_retry():
    return retry(wait=wait_fixed(1), stop=stop_after_attempt(3))


@runtime_checkable
class TelegramMessage(Protocol):
    async def reply_telegram(self, update: Update) -> None:
        pass


@runtime_checkable
class DiscordMessage(Protocol):
    async def reply_discord(self, ctx: Context) -> None:
        pass


@runtime_checkable
class BotMessage(TelegramMessage, DiscordMessage, Protocol):
    pass


@dataclass
class TextMessage(BotMessage):
    text: str

    @with_retry()
    async def reply_telegram(self, update):
        await update.message.reply_text(text=self.text[:4096])

    @with_retry()
    async def reply_discord(self, ctx):
        await ctx.reply(self.text[:2000])


@dataclass
class ImageMessage(BotMessage):
    image: BytesIO
    caption: str | None = None

    @with_retry()
    async def reply_telegram(self, update):
        await update.message.reply_photo(photo=self.image, caption=self.caption[:4096] if self.caption else None)

    @with_retry()
    async def reply_discord(self, ctx):
        file_ = discord.File(self.image, filename="image.png")
        await ctx.reply(file=file_, content=self.caption[:2000] if self.caption else None)


@dataclass
class ImageAlbumMessage(BotMessage):
    images: list[BytesIO]
    caption: str | None = None

    @with_retry()
    async def reply_telegram(self, update):
        medias = [InputMediaPhoto(image) for image in self.images]
        await update.message.reply_media_group(media=medias, caption=self.caption[:4096] if self.caption else None)

    @with_retry()
    async def reply_discord(self, ctx):
        files = [discord.File(image, filename=f"image{i}.png") for i, image in enumerate(self.images)]
        await ctx.reply(files=files, content=self.caption[:2000] if self.caption else None)


@dataclass
class FileMessage(BotMessage):
    file_: BytesIO
    filename: str
    caption: str | None = None

    @with_retry()
    async def reply_telegram(self, update):
        caption = self.caption[:4096] if self.caption else None
        await update.message.reply_document(document=self.file_, filename=self.filename, caption=caption)

    @with_retry()
    async def reply_discord(self, ctx):
        file_ = discord.File(self.file_, filename=self.filename)
        await ctx.reply(file=file_, content=self.caption[:2000] if self.caption else None)
