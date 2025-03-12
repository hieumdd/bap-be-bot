from abc import ABC
import contextlib
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json
import time

import bytewax.operators as op
import bytewax.operators.windowing as win
from bytewax.dataflow import Dataflow
from bytewax.inputs import DynamicSource, StatelessSourcePartition
from bytewax.outputs import DynamicSink, StatelessSinkPartition
from bytewax.operators.windowing import EventClock, SessionWindower
import pandas as pd
from pydantic import ValidationError
from tqdm import trange, tqdm

from logger import get_logger
from vectorstore import vectorstore
from models.message import Message, MessageRepository
from models.conversation import Conversation

logger = get_logger(__name__)


@dataclass
class MigrationInputOptions:
    chat_id: int
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
        messages = []
        for message_dict in extract_data["messages"]:
            if message_dict["type"] != "message":
                continue
            text = self.process_text(message_dict["text"])
            with contextlib.suppress(ValidationError):
                message = Message(
                    chat_id=self.chat_id,
                    id=message_dict["id"],
                    timestamp=int(message_dict["date_unixtime"]),
                    text=text,
                    from_=message_dict["from"],
                )
                messages.append(message)
        self.is_done = True
        return messages

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


@dataclass
class RedisInputOptions(RedisIOOptions):
    pass


class RedisInput(StatelessSourcePartition):
    def __init__(self, options: RedisInputOptions, repository=MessageRepository):
        self.desc = options.desc
        self.repository = repository()

    def next_batch(self):
        logger.debug("Polling from Redis")
        messages = self.repository.read()
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
    batch_size: int = 100


class RedisOutput(StatelessSinkPartition):
    def __init__(self, options: RedisOutputOptions, repository=MessageRepository):
        self.desc = options.desc
        self.batch_size = options.batch_size
        self.repository = repository()
        self.pipe = self.repository.pipeline()

    def write_batch(self, items: list[Message]):
        for i in trange(0, len(items), self.batch_size, desc=self.desc):
            batch_items = items[i : i + self.batch_size]
            self.repository.write(*batch_items, pipe=self.pipe)

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
    batch_size: int = 64
    delay: int = 5


class VectorStoreOutput(StatelessSinkPartition):
    def __init__(self, options: VectorStoreOutputOptions, vectorstore=vectorstore):
        self.desc = options.desc
        self.batch_size = options.batch_size
        self.delay = options.delay
        self.vectorstore = vectorstore()

    def write_batch(self, rows: list[Conversation]):
        sorted_rows = sorted(rows, key=lambda x: len(x.texts), reverse=True)
        num_chunks = (len(rows) + self.batch_size - 1) // self.batch_size
        chunks: list[list[Conversation]] = [[] for _ in range(num_chunks)]
        chunk_lengths = [0] * num_chunks

        for row in sorted_rows:
            min_idx = chunk_lengths.index(min(chunk_lengths))
            chunks[min_idx].append(row)
            chunk_lengths[min_idx] = chunk_lengths[min_idx] + len(row.texts)

        for chunk in tqdm(chunks, desc=self.desc):
            self.vectorstore.add_texts(
                ids=[i.id for i in chunk],
                texts=[i.texts for i in chunk],
                metadatas=chunk,
            )
            time.sleep(self.delay)


class VectorStoreSink(DynamicSink):
    def __init__(self, options: VectorStoreOutputOptions):
        self.options = options

    def build(self, *args):
        return VectorStoreOutput(self.options)


def transform_to_conversation(items: tuple[str, tuple[str, list[Message]]]):
    chat_id, data = items
    _, messages = data

    df = (
        pd.DataFrame(map(lambda m: m.model_dump(by_alias=True), messages))
        .drop_duplicates()
        .sort_values("timestamp")
    )
    df["text"] = df["from"] + ": " + df["text"]

    conversation_id = int(df["timestamp"].min())
    conversation = Conversation(
        chat_id=int(chat_id),
        conversation_id=conversation_id,
        start_timestamp=int(df["timestamp"].min()),
        end_timestamp=int(df["timestamp"].max()),
        texts="\n".join(df["text"].astype(str).to_list()),
    )
    return conversation


migrate = Dataflow("message")
message_stream1 = op.input(
    "input1",
    migrate,
    MigrationSource(
        MigrationInputOptions(859761464, "./migrations/customer-journey.json")
    ),
)
message_stream2 = op.input(
    "input2",
    migrate,
    MigrationSource(MigrationInputOptions(1001863500354, "./migrations/hop-lop.json")),
)
merged_stream = op.merge("merge", message_stream1, message_stream2)
op.output(
    "output",
    merged_stream,
    RedisSink(RedisOutputOptions("Writing Messages to Redis")),
)


embed = Dataflow("conversation")
conversation_stream = op.input(
    "input",
    embed,
    RedisSource(RedisInputOptions("Transfering Messages on Redis")),
)
keyed_conversation = op.key_on(
    "group_by_chat_id",
    conversation_stream,
    lambda m: str(m.chat_id),
)
windowed_conversation = win.collect_window(
    "window_by_conversation_id",
    keyed_conversation,
    EventClock(
        lambda m: datetime.fromtimestamp(m.timestamp, timezone.utc),
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
