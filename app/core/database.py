from pymongo import MongoClient

from app.core.settings import Settings


class MongoDBService:
    client: MongoClient

    def __init__(self, settings: Settings):
        self.client = MongoClient(settings.mongodb_uri)

    def __enter__(self) -> MongoClient:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        return False
