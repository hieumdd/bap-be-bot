import hashlib
import uuid

from pydantic import BaseModel, ConfigDict, computed_field


class Conversation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    chat_id: int
    conversation_id: int
    start_timestamp: int
    end_timestamp: int
    texts: str

    @computed_field
    @property
    def id(self) -> str:
        combined_bytes = f"{self.chat_id}-{self.conversation_id}".encode()
        hash_bytes = hashlib.md5(combined_bytes).digest()
        return str(uuid.UUID(bytes=hash_bytes))
