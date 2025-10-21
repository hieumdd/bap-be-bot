from dataclasses import dataclass
from typing import Optional

from redis.client import Pipeline

from app.core.settings import config
from app.core.db import redis_client
from app.rag.message_model import Message


@dataclass
class MessageRepository:
    key: str

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


message_repository = MessageRepository(config.message_repository_key)
