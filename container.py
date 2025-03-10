from dependency_injector import containers, providers
from langchain_core.embeddings import Embeddings as IEmbeddings
from langchain_core.language_models import BaseLLM as ILLM
from langchain_core.prompts import PromptTemplate as IPromptTemplate
from langchain_core.vectorstores import VectorStore as IVectorStore
from pydantic_settings import BaseSettings, SettingsConfigDict

from db import DB
from embedding import Embedding
from llm import LLM
from prompt import Prompt
from rag import RAG
from vectorstore import VectorStore


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    qdrant_url: str
    redis_url: str
    google_api_key: str
    pinecone_api_key: str
    telegram_bot_token: str

    database_key: str = "message"
    vectorstore_key: str = "conversation"
    embedding: str = "multilingual_e5_large"


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[Settings()])

    db = providers.Container(DB, config=config)

    embedding_package = providers.Container(Embedding, config=config)
    embedding: providers.Provider[IEmbeddings] = embedding_package.embedding

    vectorstore_package = providers.Container(
        VectorStore,
        config=config,
        db=db,
        embedding=embedding,
    )
    vectorstore: providers.Provider[IVectorStore] = vectorstore_package.qdrant

    llm_container = providers.Container(LLM, config=config)
    llm: providers.Provider[ILLM] = llm_container.gemini_20_flash_lite

    prompt_container = providers.Container(Prompt)
    prompt: providers.Provider[IPromptTemplate] = prompt_container.conversation

    rag = providers.Singleton(RAG, vectorstore=vectorstore, llm=llm, prompt=prompt)
