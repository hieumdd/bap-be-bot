from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from redis.client import Pipeline

from config import Config
from db import redis_client


class Message(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    chat_id: int
    id: int
    timestamp: int
    text: str = Field(min_length=1)
    from_: str = Field(alias="from")


class MessageRepository:
    def __init__(self, config=Config, redis_client=redis_client):
        self.key = config().message_repository_key
        self.redis = redis_client()

    def read(self) -> list[Message]:
        count = self.redis.llen(self.key)
        if not count:
            return []
        message_raw = self.redis.lpop(self.key, count)
        return [Message.model_validate_json(m) for m in message_raw]

    def write(self, *messages: list[Message], pipe: Optional[Pipeline] = None):
        executor = pipe or self.redis
        executor.rpush(
            self.key,
            *map(lambda m: m.model_dump_json(by_alias=True), messages),
        )

    def pipeline(self) -> Pipeline:
        return self.redis.pipeline()
