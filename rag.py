from datetime import datetime
import re
from textwrap import dedent

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
from config import config
from vectorstore import vectorstore

logger = get_logger(__name__)

chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY: HarmBlockThreshold.BLOCK_NONE,
    },
    google_api_key=config.google_api_key,
)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            dedent(
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
        ),
        HumanMessagePromptTemplate.from_template(
            dedent(
                """
                ### Provided Conversations:
                {context}

                ### Prompt:
                {query}
                """
            )
        ),
    ]
)


async def answer(query: str, k=10, lambda_mult=0.3):
    def format_docs(docs: list[Document]):
        conversations = [
            dedent(
                f"""
                <CONVERSATION>
                Start: {datetime.fromtimestamp(c.metadata["start_timestamp"]).strftime("%Y-%m-%d")}
                End: {datetime.fromtimestamp(c.metadata["end_timestamp"]).strftime("%Y-%m-%d")}
                Messages:
                {c.metadata["texts"]}
                </CONVERSATION>"""
            )
            for c in docs
        ]
        return "\n".join(conversations)

    def format_html(message: AIMessage):
        text = re.sub(r"\*\*(.*?)\*\*|__(.*?)__", r"<b>\1\2</b>", message.content)
        text = re.sub(r"\*(.*?)\*|_(.*?)_", r"<i>\1\2</i>", text)
        return dedent(text)

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
    chain = (
        {"context": retriever | format_docs, "query": RunnablePassthrough()}
        | prompt
        | chat_model
        | format_html
    )

    logger.debug(f"Answering Query: {query}")
    response = await chain.ainvoke(f"query: {query}")
    return response
