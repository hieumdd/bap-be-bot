from dataclasses import dataclass
from io import BytesIO
from typing import Protocol, runtime_checkable

import discord
from discord.ext.commands.context import Context
from telegram import InputMediaPhoto, Update
from telegram.constants import ChatAction, MessageLimit
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
        await update.message.reply_chat_action(ChatAction.TYPING)
        await update.message.reply_text(text=self.text[:MessageLimit.MAX_TEXT_LENGTH], reply_to_message_id=update.message.id)

    @with_retry()
    async def reply_discord(self, ctx):
        async with ctx.typing():
            await ctx.reply(self.text[:2000])


@dataclass
class ImageMessage(BotMessage):
    image: BytesIO
    caption: str | None = None

    @with_retry()
    async def reply_telegram(self, update):
        await update.message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
        await update.message.reply_photo(
            photo=self.image,
            caption=self.caption[:MessageLimit.CAPTION_LENGTH] if self.caption else None,
            reply_to_message_id=update.message.id,
        )

    @with_retry()
    async def reply_discord(self, ctx):
        file_ = discord.File(self.image, filename="image.png")
        async with ctx.typing():
            await ctx.reply(file=file_, content=self.caption[:2000] if self.caption else None)


@dataclass
class ImageAlbumMessage(BotMessage):
    images: list[BytesIO]
    caption: str | None = None

    @with_retry()
    async def reply_telegram(self, update):
        await update.message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
        medias = [InputMediaPhoto(image) for image in self.images]
        await update.message.reply_media_group(
            media=medias,
            caption=self.caption[:MessageLimit.CAPTION_LENGTH] if self.caption else None,
            reply_to_message_id=update.message.id,
        )

    @with_retry()
    async def reply_discord(self, ctx):
        files = [discord.File(image, filename=f"image{i}.png") for i, image in enumerate(self.images)]
        async with ctx.typing():
            await ctx.reply(files=files, content=self.caption[:2000] if self.caption else None)


@dataclass
class FileMessage(BotMessage):
    file_: BytesIO
    filename: str
    caption: str | None = None

    @with_retry()
    async def reply_telegram(self, update):
        await update.message.reply_chat_action(ChatAction.UPLOAD_DOCUMENT)
        await update.message.reply_document(
            document=self.file_,
            filename=self.filename,
            caption=self.caption[:MessageLimit.CAPTION_LENGTH] if self.caption else None,
            reply_to_message_id=update.message.id,
        )

    @with_retry()
    async def reply_discord(self, ctx):
        file_ = discord.File(self.file_, filename=self.filename)
        async with ctx.typing():
            await ctx.reply(file=file_, content=self.caption[:2000] if self.caption else None)
