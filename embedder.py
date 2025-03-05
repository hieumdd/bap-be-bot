import asyncio
from datetime import datetime, timedelta, timezone
import json

import bytewax.operators as op
import bytewax.operators.windowing as win
from bytewax.dataflow import Dataflow
from bytewax.inputs import DynamicSource, StatelessSourcePartition
from bytewax.outputs import DynamicSink, StatelessSinkPartition
from bytewax.operators.windowing import EventClock, SessionWindower
import pandas as pd
from tqdm.asyncio import tqdm_asyncio

from logger import get_logger
from db import REDIS_CLIENT
from rag import RAG

logger = get_logger(__name__)


class MigrationInput(StatelessSourcePartition):
    def __init__(self, chat_id: str, file_path: str):
        self.chat_id = chat_id
        self.file = open(file_path, "r")
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
    def __init__(self, chat_id: str, file_path: str):
        self.chat_id = chat_id
        self.file_path = file_path

    def build(self, *args):
        return MigrationInput(self.chat_id, self.file_path)


class RedisInput(StatelessSourcePartition):
    def __init__(self, key: str):
        self.key = key

    def next_batch(self):
        logger.debug("Polling from Redis")
        messages_bytes = REDIS_CLIENT.lrange(self.key, 0, -1)
        if not messages_bytes:
            return []
        messages = list(map(lambda x: json.loads(x.decode("utf-8")), messages_bytes))
        return messages

    def next_awake(self):
        return datetime.now(timezone.utc) + timedelta(seconds=5)


class RedisSource(DynamicSource):
    def __init__(self, key: str):
        self.key = key

    def build(self, *args):
        return RedisInput(self.key)


class ChromaDBOutput(StatelessSinkPartition):
    def __init__(self, collection_name: str, batch_size=10):
        self.vector_store = RAG.create_vector_store(collection_name)
        self.batch_size = batch_size

    def write_batch(self, rows):
        async def upsert(batch_rows):
            try:
                await self.vector_store.aadd_texts(
                    texts=[x["texts"] for x in batch_rows],
                    ids=[x["conversation_id"] for x in batch_rows],
                    metadatas=batch_rows,
                )
            except Exception as e:
                logger.warning(e)

        async def upsert_batch():
            tasks = [
                asyncio.create_task(upsert(rows[i : i + self.batch_size]))
                for i in range(0, len(rows), self.batch_size)
            ]
            await tqdm_asyncio.gather(*tasks, desc="Processing Batches", unit="batch")

        asyncio.run(upsert_batch())


class ChromaDBSink(DynamicSink):
    def __init__(self, collection_name: str, batch_size=100):
        self.collection_name = collection_name
        self.batch_size = batch_size

    def build(self, *args):
        return ChromaDBOutput(self.collection_name)


class RedisOutput(StatelessSinkPartition):
    def __init__(self, key: str):
        self.key = key

    def write_batch(self, items):
        for item in items:
            REDIS_CLIENT.rpush(self.key, json.dumps(item))


class RedisSink(DynamicSink):
    def __init__(self, key: str):
        self.key = key

    def build(self, *args):
        return RedisOutput(self.key)


def parse_message(message):
    timestamp = datetime.fromtimestamp(message["timestamp"], timezone.utc)
    return {**message, "timestamp": timestamp}


def transform_to_conversation(items):
    chat_id, data = items
    _, messages = data

    df = pd.DataFrame(messages).drop_duplicates()
    df["timestamp"] = df["timestamp"].apply(lambda x: int(x.timestamp()))
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


message_flow = Dataflow("message")
message_stream1 = op.input(
    "input1",
    message_flow,
    MigrationSource("859761464", "./migrations/customer-journey.json"),
)
message_stream2 = op.input(
    "input2",
    message_flow,
    MigrationSource("1001863500354", "./migrations/hop-lop.json"),
)
merged_stream = op.merge("merge", message_stream1, message_stream2)
op.output("output", merged_stream, RedisSink("message"))

conversation_flow = Dataflow("conversation")
conversation_stream = op.input(
    "input",
    conversation_flow,
    RedisSource("message"),
)
parsed_conversation = op.map("parse", conversation_stream, parse_message)
keyed_conversation = op.key_on(
    "group_by_chat_id",
    parsed_conversation,
    lambda x: x["chat_id"],
)
windowed_conversation = win.collect_window(
    "window_by_conversation_id",
    keyed_conversation,
    EventClock(lambda x: x["timestamp"], wait_for_system_duration=timedelta(minutes=5)),
    SessionWindower(timedelta(seconds=7200)),
)
grouped_conversation = op.map(
    "group_by_conversation_id",
    windowed_conversation.down,
    transform_to_conversation,
)
# op.inspect("debug_group_by_conversation_id", grouped_conversation, inspector)
op.output("output", grouped_conversation, ChromaDBSink("telegram"))
