from pydantic import BaseModel
from telegram import Update


class TelegramUser(BaseModel):
    id: int
    chat_id: int
    full_name: str

    @property
    def _id(self) -> dict[str, int]:
        return {"id": self.id, "chat_id": self.chat_id}

    @classmethod
    def from_update(cls, update: Update):
        return cls(
            id=update.effective_user.id,
            chat_id=update.effective_chat.id,
            full_name=update.effective_user.full_name,
        )
