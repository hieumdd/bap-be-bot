import random
from textwrap import dedent

from langchain.schema import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

from app.core.llm import chat_model
from app.tarot.tarot_state import TarotState, TarotAnalyzeState
from app.tarot.tarot_card_model import tarot_cards
from app.tarot.tarot_telling_card_model import TarotTellingCard


def randomize_tarot_cards(state: TarotState):
    tarot_telling_cards: list[TarotTellingCard] = []
    for tarot_card in random.sample(tarot_cards, 3):
        is_reversed = random.choice([True, False])
        ttc = TarotTellingCard(
            name=tarot_card.name,
            is_reversed=is_reversed,
            meaning=tarot_card.meaning_rev if is_reversed else tarot_card.meaning,
            image=tarot_card.get_image_rev() if is_reversed else tarot_card.get_image(),
        )
        tarot_telling_cards.append(ttc)
    return {"tarot_telling_cards": tarot_telling_cards}


def analyze_card(state: TarotAnalyzeState):
    system_message = SystemMessage(
        content=dedent(
            """
            Bạn là một nhà chiêm tinh và chuyên gia Tarot. Sử dụng lá Tarot và câu hỏi của người dùng, hãy phân tích và đưa ra những nhận định.
            Ngoài ra không đưa ra thông tin gì thêm
            Đưa ra Kết quả phân tích theo định dạng
            Lá bài: <lá bài>
            Phân tích: <phân tích>
            """
        )
    )
    tarot_human_message = HumanMessagePromptTemplate.from_template(
        dedent(
            """
            Lá Tarot: {tarot_telling_card_name}
            Đảo ngược: {tarot_telling_card_is_reversed}
            Ý nghĩa: {tarot_telling_card_meaning}
            """
        )
    )
    question_human_message = HumanMessagePromptTemplate.from_template(
        "Câu hỏi: {question}"
    )
    messages = [system_message, tarot_human_message, question_human_message]
    prompt = ChatPromptTemplate.from_messages(messages)
    chain = prompt | chat_model
    analysis = chain.invoke(
        {
            "question": state["question"],
            "tarot_telling_card_name": state["tarot_telling_card"].name,
            "tarot_telling_card_is_reversed": state["tarot_telling_card"].is_reversed,
            "tarot_telling_card_meaning": state["tarot_telling_card"].meaning,
        }
    )
    return {"messages": [analysis], "analysis": [analysis.content]}
