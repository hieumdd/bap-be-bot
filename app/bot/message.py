from dataclasses import dataclass
import io
from typing import Protocol, runtime_checkable

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
class TextMessage(TelegramMessage):
    html: str

    @with_retry()
    async def reply_telegram(self, update):
        await update.message.reply_text(text=self.html[:4096])


@dataclass
class ImageMessage(TelegramMessage):
    caption: str
    image: io.BytesIO

    @with_retry()
    async def reply_telegram(self, update):
        await update.message.reply_photo(photo=self.image, caption=self.caption[:4096])


@dataclass
class ImageAlbumMessage(TelegramMessage):
    caption: str
    images: list[io.BytesIO]

    @with_retry()
    async def reply_telegram(self, update):
        medias = [InputMediaPhoto(image) for image in self.images]
        await update.message.reply_media_group(media=medias, caption=self.caption[:4096])


@dataclass
class FileMessage(TelegramMessage):
    caption: str
    filename: str
    file_: io.BytesIO

    @with_retry()
    async def reply_telegram(self, update):
        await update.message.reply_document(document=self.file_, filename=self.filename, caption=self.caption)
