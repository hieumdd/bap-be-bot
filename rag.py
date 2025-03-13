from datetime import datetime
from functools import lru_cache
import re

from langchain.schema import AIMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmCategory,
    HarmBlockThreshold,
)

from logger import get_logger
from config import Config
from vectorstore import vectorstore

logger = get_logger(__name__)


@lru_cache(1)
def llm(config=Config):
    logger.debug("Initialized LLM")
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY: HarmBlockThreshold.BLOCK_NONE,
        },
        google_api_key=config().google_api_key,
    )


@lru_cache(1)
def prompt():
    logger.debug("Initialized Prompt")
    system = SystemMessagePromptTemplate.from_template(
        """
        You are Bot Bập Bẹ, a smart AI tasked with analyzing conversation & answering questions based on provided context. Here are multiple relevent conversations betweens friends within group chats as context.
        Each conversation is between XML tag <CONVERSATION> and </CONVERSATION>
        Each conversation is formatted with this structure:
        Start: YYYY-MM-DD (Start of the conversation)
        End: YYYY-MM-DD (End of the conversation)
        Messages: str (Messages, each message are seperated by newline, in the form of [Sender]: [Text])

        ### Answer Requirements
        - Provide detailed analysis based on evidence from conversations
        - Provide quotation or proofs
        - ONLY ANSWER IN THE PROMPT'S LANGUAGE

        ### Answer Formatting Requirements
        - Each section contains no more than 4096 character
        - Each bullet point should be continous without empty line in between
        """
    )
    human = HumanMessagePromptTemplate.from_template(
        """
        ### Provided Conversations:
        {context}

        ### Prompt:
        {query}
        """
    )
    return ChatPromptTemplate.from_messages([system, human])


async def answer(
    query: str,
    k=10,
    lambda_mult=0.3,
    vectorstore=vectorstore,
    prompt=prompt,
    llm=llm,
):
    def format_docs(docs: list[Document]):
        conversations = [
            f"""<CONVERSATION>
            Start: {datetime.fromtimestamp(c.metadata["start_timestamp"]).strftime("%Y-%m-%d")}
            End: {datetime.fromtimestamp(c.metadata["end_timestamp"]).strftime("%Y-%m-%d")}
            Messages:
            {c.page_content}
            </CONVERSATION>"""
            for c in docs
        ]
        return "\n".join(conversations)

    def format_html(message: AIMessage):
        text = re.sub(r"\*\*(.*?)\*\*|__(.*?)__", r"<b>\1\2</b>", message.content)
        message = re.sub(r"\*(.*?)\*|_(.*?)_", r"<i>\1\2</i>", text)
        return message

    retriever = vectorstore().as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "lambda_mult": lambda_mult},
    )
    chain = (
        {"context": retriever | format_docs, "query": RunnablePassthrough()}
        | prompt()
        | llm()
        | format_html
    )

    logger.debug(f"Answering Query: {query}")
    response = await chain.ainvoke(query)
    return response
