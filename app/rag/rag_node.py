from datetime import datetime
import re
from textwrap import dedent

from langchain.schema import AIMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough

from logger import get_logger
from app.core.llm import chat_model
from app.rag.rag_vectorstore import vectorstore
from app.rag.rag_state import RagState

logger = get_logger(__name__)


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
    messages = [AIMessage(dedent(c)) for c in text.split("\n\n") if c]
    return messages


def rag(state: RagState):
    system_message = SystemMessagePromptTemplate.from_template(
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
    )
    human_message = HumanMessagePromptTemplate.from_template(
        dedent(
            """
            ### Provided Conversations:
            {context}

            ### Prompt:
            {query}
            """
        )
    )
    prompt = ChatPromptTemplate.from_messages([system_message, human_message])
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10},
    )
    chain = (
        {"context": retriever | format_docs, "query": RunnablePassthrough()}
        | prompt
        | chat_model
        | format_html
    )
    messages = chain.invoke(f"query: {state["messages"][0].content}")
    return {"messages": state["messages"] + messages}
