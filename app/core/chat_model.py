from abc import ABC
from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold

from app.core.settings import Settings


class ChatModelService:
    def __init__(self, settings: Settings, model="gemini-2.0-flash", temperature=1.0):
        settings = settings or Settings()
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY: HarmBlockThreshold.BLOCK_NONE,
        }
        self.chat_model = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            safety_settings=safety_settings,
            google_api_key=settings.google_api_key,
        )


class ChatModelNode(ABC):
    chat_model_service: ChatModelService

    def __init__(self, chat_model_service: ChatModelService):
        self.chat_model_service = chat_model_service
