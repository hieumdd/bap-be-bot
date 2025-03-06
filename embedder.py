from abc import ABC
import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json

import bytewax.operators as op
import bytewax.operators.windowing as win
from bytewax.dataflow import Dataflow
from bytewax.inputs import DynamicSource, StatelessSourcePartition
from bytewax.outputs import DynamicSink, StatelessSinkPartition
from bytewax.operators.windowing import EventClock, SessionWindower
from dependency_injector.wiring import Provide, inject
import pandas as pd
from redis import Redis
from tqdm import trange
from tqdm.asyncio import tqdm_asyncio

from logger import get_logger
from container import Container
from vectorstore import CustomVectorStore

logger = get_logger(__name__)


@dataclass
class MigrationInputOptions:
    chat_id: str
    file_path: str


class MigrationInput(StatelessSourcePartition):
    def __init__(self, options: MigrationInputOptions):
        self.chat_id = options.chat_id
        self.file = open(options.file_path, "r")
        self.is_done = False

    def process_text(self, v: str | list[str]):
        if isinstance(v, str):
            return v
        ts = []
        for t in v:
            if isinstance(t, str):
                ts.append(t)
            elif t.get("type") == "bot_command":
                return ""
            else:
                ts.append(t["text"])
        return "".join(ts)

    def next_batch(self):
        if self.is_done:
            raise StopIteration()

        extract_data = json.load(self.file)
        rows = []
        for message in extract_data["messages"]:
            if message["type"] != "message":
                continue
            text = self.process_text(message["text"])
            if not text:
                continue
            row = {
                "chat_id": self.chat_id,
                "id": message["id"],
                "text": text,
                "timestamp": int(message["date_unixtime"]),
                "from": message["from"],
            }
            rows.append(row)
        self.is_done = True
        return rows

    def close(self):
        self.file.close()


class MigrationSource(DynamicSource):
    def __init__(self, options: MigrationInputOptions):
        self.options = options

    def build(self, *args):
        return MigrationInput(self.options)


@dataclass
class RedisIOOptions(ABC):
    desc: str
    batch_size: int = 100


@dataclass
class RedisInputOptions(RedisIOOptions):
    pass


class RedisInput(StatelessSourcePartition):
    def __init__(self, options: RedisInputOptions):
        self.batch_size = options.batch_size
        self.desc = options.desc

    @inject
    def next_batch(
        self,
        key: str = Provide[Container.config.database_key],
        redis: Redis = Provide[Container.db.redis],
    ):
        logger.debug("Polling from Redis")
        messages_bytes = redis.lrange(key, 0, -1)
        if not messages_bytes:
            return []
        with redis.pipeline() as pipe:
            for i in trange(0, len(messages_bytes), self.batch_size, desc=self.desc):
                batch_messages_bytes = messages_bytes[i : i + self.batch_size]
                pipe.rpush(f"{key}-cumulative", *batch_messages_bytes)
            pipe.delete(key)
            pipe.execute()
        messages = list(map(lambda x: json.loads(x.decode("utf-8")), messages_bytes))
        return messages

    def next_awake(self):
        return datetime.now(timezone.utc) + timedelta(seconds=5)


class RedisSource(DynamicSource):
    def __init__(self, options: RedisInputOptions):
        self.options = options

    def build(self, *args):
        return RedisInput(self.options)


@dataclass
class RedisOutputOptions(RedisIOOptions):
    pass


class RedisOutput(StatelessSinkPartition):
    @inject
    def __init__(
        self,
        options: RedisOutputOptions,
        redis: Redis = Provide[Container.db.redis],
    ):
        self.batch_size = options.batch_size
        self.desc = options.desc
        self.pipe = redis.pipeline()

    def write_batch(
        self,
        items: list[dict],
        key: str = Provide[Container.config.database_key],
    ):
        for i in trange(0, len(items), self.batch_size, desc=self.desc):
            batch_items = items[i : i + self.batch_size]
            self.pipe.rpush(key, *map(json.dumps, batch_items))

    def close(self):
        self.pipe.execute()


class RedisSink(DynamicSink):
    def __init__(self, options: RedisOutputOptions):
        self.options = options

    def build(self, *args):
        return RedisOutput(self.options)


@dataclass
class VectorStoreOutputOptions:
    desc: str
    batch_size: int = 10
    concurrency: int = 5


class VectorStoreOutput(StatelessSinkPartition):
    @inject
    def __init__(
        self,
        options: VectorStoreOutputOptions,
        vectorstore: CustomVectorStore = Provide[Container.vectorstore],
    ):
        self.desc = options.desc
        self.batch_size = options.batch_size
        self.concurrency = options.concurrency
        self.vectorstore = vectorstore

    def write_batch(self, rows: list[dict]):

        async def upsert(batch_rows: list[dict], sem: asyncio.Semaphore):
            try:
                async with sem:
                    await self.vectorstore.upsert(batch_rows)
            except Exception as e:
                logger.warning(e)

        async def upsert_batch():
            sem = asyncio.Semaphore(self.concurrency)
            tasks = [
                asyncio.create_task(upsert(rows[i : i + self.batch_size], sem))
                for i in range(0, len(rows), self.batch_size)
            ]
            await tqdm_asyncio.gather(*tasks, desc=self.desc)

        asyncio.run(upsert_batch())


class VectorStoreSink(DynamicSink):
    def __init__(self, options: VectorStoreOutputOptions):
        self.options = options

    def build(self, *args):
        return VectorStoreOutput(self.options)


def transform_to_conversation(items: tuple[str, tuple[str, list[dict]]]):
    chat_id, data = items
    _, messages = data

    df = pd.DataFrame(messages).drop_duplicates().sort_values("timestamp")
    df["text"] = df["from"] + ": " + df["text"]

    conversation_id = str(df["timestamp"].min())
    conversation = {
        "chat_id": chat_id,
        "conversation_id": conversation_id,
        "start_timestamp": int(df["timestamp"].min()),
        "end_timestamp": int(df["timestamp"].max()),
        "texts": "\n".join(df["text"].astype(str).to_list()),
    }
    return conversation


container = Container()
container.wire(modules=[__name__])

message_flow = Dataflow("message")
message_stream1 = op.input(
    "input1",
    message_flow,
    MigrationSource(
        MigrationInputOptions("859761464", "./migrations/customer-journey.json")
    ),
)
message_stream2 = op.input(
    "input2",
    message_flow,
    MigrationSource(
        MigrationInputOptions("1001863500354", "./migrations/hop-lop.json")
    ),
)
merged_stream = op.merge("merge", message_stream1, message_stream2)
op.output(
    "output",
    merged_stream,
    RedisSink(RedisOutputOptions("Writing Messages to Redis")),
)


conversation_flow = Dataflow("conversation")
conversation_stream = op.input(
    "input",
    conversation_flow,
    RedisSource(RedisInputOptions("Transfering Messages on Redis")),
)
keyed_conversation = op.key_on(
    "group_by_chat_id",
    conversation_stream,
    lambda x: x["chat_id"],
)
windowed_conversation = win.collect_window(
    "window_by_conversation_id",
    keyed_conversation,
    EventClock(
        lambda x: datetime.fromtimestamp(x["timestamp"], timezone.utc),
        wait_for_system_duration=timedelta(seconds=30),
    ),
    SessionWindower(timedelta(seconds=7200)),
)
grouped_conversation = op.map(
    "group_by_conversation_id",
    windowed_conversation.down,
    transform_to_conversation,
)
op.output(
    "output",
    grouped_conversation,
    VectorStoreSink(
        VectorStoreOutputOptions("Upserting Conversations to Vector Store")
    ),
)
