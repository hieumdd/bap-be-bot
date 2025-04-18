import contextlib
from datetime import datetime, timedelta, timezone
import json
import pathlib

import bytewax.operators as op
import bytewax.operators.windowing as win
from bytewax.dataflow import Dataflow
from bytewax.inputs import DynamicSource, StatelessSourcePartition
from bytewax.outputs import DynamicSink, StatelessSinkPartition
from bytewax.operators.windowing import EventClock, SessionWindower
import pandas as pd
from pydantic import ValidationError
from tqdm import trange

from logger import get_logger
from app.rag.rag_vectorstore import vectorstore
from app.rag.message_model import Message
from app.rag.message_repository import message_repository
from app.rag.conversation_model import Conversation

logger = get_logger(__name__)


class MigrationInput(StatelessSourcePartition):
    def __init__(self, file_path: str):
        path = pathlib.Path(file_path)
        self.chat_id = int(path.stem)
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
    def __init__(self, file_path: str):
        self.file_path = file_path

    def build(self, *args):
        return MigrationInput(self.file_path)


class RedisInput(StatelessSourcePartition):
    def next_batch(self):
        logger.debug("Polling from Redis")
        messages = message_repository.read()
        return messages

    def next_awake(self):
        return datetime.now(timezone.utc) + timedelta(seconds=5)


class RedisSource(DynamicSource):
    def build(self, *args):
        return RedisInput()


class RedisOutput(StatelessSinkPartition):
    desc: str = "Writing Messages to Redis"
    batch_size: int = 100

    def __init__(self):
        self.pipe = message_repository.pipeline()

    def write_batch(self, items: list[Message]):
        for i in trange(0, len(items), self.batch_size, desc=self.desc):
            batch_items = items[i : i + self.batch_size]
            message_repository.write(*batch_items, pipe=self.pipe)

    def close(self):
        self.pipe.execute()


class RedisSink(DynamicSink):
    def build(self, *args):
        return RedisOutput()


class VectorStoreOutput(StatelessSinkPartition):
    desc: str = "Upserting Conversations to Vector Store"
    batch_size: int = 20

    def write_batch(self, rows: list[Conversation]):
        for i in trange(0, len(rows), self.batch_size, desc=self.desc):
            batch_rows = rows[i : i + self.batch_size]
            vectorstore.add_texts(
                ids=[i.id for i in batch_rows],
                texts=[f"passage: {i.texts}" for i in batch_rows],
                metadatas=batch_rows,
            )
        #     tasks.append(asyncio.create_task(coro))
        #     if len(tasks) % 200 == 0:
        #         await asyncio.sleep(self.delay)
        # async def upsert_batch():
        #     tasks = []
        #     for task in tqdm_asyncio.as_completed(tasks, desc=self.desc):
        #         await task

        # asyncio.run(upsert_batch())


class VectorStoreSink(DynamicSink):
    def build(self, *args):
        return VectorStoreOutput()


def sort_message(items):
    return sorted(items, key=lambda x: x.timestamp)


def reduce_by_conversation(items: tuple[str, tuple[str, list[Message]]]):
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


migrate = Dataflow("migrate")
migrate_input1 = op.input(
    "input1",
    migrate,
    MigrationSource("./migrations/859761464.json"),
)
migrate_input2 = op.input(
    "input2",
    migrate,
    MigrationSource("./migrations/1001863500354.json"),
)
migrate_merged = op.merge("merge", migrate_input1, migrate_input2)
migrate_keyed = op.key_on("key", migrate_merged, lambda _: "ALL")
migrate_folded = op.fold_final(
    "fold",
    migrate_keyed,
    lambda: [],
    lambda acc, cur: acc + [cur],
)
migrate_keyrm = op.key_rm("key_rm", migrate_folded)
migrate_sorted = op.flat_map(
    "sort",
    migrate_keyrm,
    lambda messages: sorted(messages, key=lambda m: m.timestamp),
)
op.output("output", migrate_sorted, RedisSink())


embed = Dataflow("embed")
embed_input = op.input("input", embed, RedisSource())
embed_keyed = op.key_on("key_on_chat_id", embed_input, lambda m: str(m.chat_id))
embed_windowed = win.collect_window(
    "window_by_session",
    embed_keyed,
    EventClock(
        lambda m: datetime.fromtimestamp(m.timestamp, timezone.utc),
        wait_for_system_duration=timedelta(seconds=30),
    ),
    SessionWindower(timedelta(seconds=7200)),
)
embed_reduced = op.map(
    "reduce_by_conversation",
    embed_windowed.down,
    reduce_by_conversation,
)
op.output("output", embed_reduced, VectorStoreSink())
