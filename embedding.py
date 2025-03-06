from dependency_injector import containers, providers
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from logger import get_logger

logger = get_logger(__name__)


class Embedding(containers.DeclarativeContainer):
    config = providers.Configuration()

    hf = providers.Singleton(
        HuggingFaceEmbeddings,
        model_name="dangvantuan/vietnamese-embedding",
    )
    gemini = providers.Singleton(
        GoogleGenerativeAIEmbeddings,
        model="models/text-embedding-004",
        google_api_key=config.google_api_key,
    )
    embedding = providers.Selector(config.embedding, hf=hf, gemini=gemini)


def get_embedding_vietnamese():
    return HuggingFaceEmbeddings(model_name="dangvantuan/vietnamese-embedding")


def get_embedding_gemini(google_api_key: str):
    return GoogleGenerativeAIEmbeddings(
        model="text-embedding-004",
        google_api_key=google_api_key,
    )
