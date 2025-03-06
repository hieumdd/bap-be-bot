from dependency_injector import containers, providers
from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold


class LLM(containers.DeclarativeContainer):
    config = providers.Configuration()

    gemini_20_flash_lite = providers.Singleton(
        GoogleGenerativeAI,
        model="gemini-2.0-flash-lite",
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY: HarmBlockThreshold.BLOCK_NONE,
        },
        google_api_key=config.google_api_key,
    )
