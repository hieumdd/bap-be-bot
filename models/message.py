from functools import lru_cache
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from redis.client import Pipeline

from config import config
from db import redis_client


class Message(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    chat_id: int
    id: int
    timestamp: int
    text: str = Field(min_length=1)
    from_: str = Field(alias="from")


@lru_cache(1)
class MessageRepository:
    def __init__(self):
        self.key = config.message_repository_key

    def read(self) -> list[Message]:
        count = redis_client.llen(self.key)
        if not count:
            return []
        message_raw = redis_client.lpop(self.key, count)
        return [Message.model_validate_json(m) for m in message_raw]

    def write(self, *messages: list[Message], pipe: Optional[Pipeline] = None):
        executor = pipe or redis_client
        executor.rpush(
            self.key,
            *map(lambda m: m.model_dump_json(by_alias=True), messages),
        )

    def pipeline(self) -> Pipeline:
        return redis_client.pipeline()
