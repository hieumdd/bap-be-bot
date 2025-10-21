import random
from textwrap import dedent

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langgraph.types import Send

from app.core.chat_model import ChatModelService
from app.tarot.tarot_state import TarotTellingState, TarotCardAnalyzeState
from app.tarot.tarot_card_model import TarotCardVariant, tarot_cards


class RandomizeTarotCards:
    count: int

    def __init__(self, count: int = 3):
        self.count = count

    def __call__(self, _: TarotTellingState):
        tcs: list[TarotCardVariant] = []
        for tarot_card in random.sample(tarot_cards, self.count):
            tc = tarot_card.variants[random.choice([0, 1])]
            tcs.append(tc)
        return TarotTellingState(tarot_cards=tcs)


class MapTarotCards:
    node: str

    def __init__(self, node: str):
        self.node = node

    def __call__(self, state: TarotTellingState):
        question = state["messages"][0].content
        return [Send(self.node, TarotCardAnalyzeState(question=question, tarot_card=tc)) for tc in state["tarot_cards"]]


class AnalyzeTarotCard:
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
            Lá Tarot: {tarot_card_name}
            Đảo ngược: {tarot_card_is_reversed}
            Ý nghĩa: {tarot_card_meaning}
            """
        )
    )
    question_human_message = HumanMessagePromptTemplate.from_template("Câu hỏi: {question}")
    messages = [system_message, tarot_human_message, question_human_message]
    prompt = ChatPromptTemplate.from_messages(messages)

    def __init__(self, chat_model_service: ChatModelService):
        self.chat_model = chat_model_service.chat_model

    def __call__(self, state: TarotCardAnalyzeState):
        chain = self.prompt | self.chat_model
        analysis: AIMessage = chain.invoke(
            {
                "question": state["question"],
                "tarot_card_name": state["tarot_card"].parent.name,
                "tarot_card_is_reversed": state["tarot_card"].is_reversed,
                "tarot_card_meaning": state["tarot_card"].meaning,
            }
        )
        return TarotTellingState(messages=[analysis], analysis=[analysis.content])


class SummarizeTarotCards:
    system_message = SystemMessage(
        content=dedent(
            """
            Bạn là một nhà chiêm tinh và chuyên gia Tarot.
            Ở tin nhắn trước bạn những lá Tarot ngẫu nhiên của một người.
            Hãy sử dụng ngữ cảnh được cung cấp (câu hỏi của người dùng & phân tích các lá Tarot)
            Đưa ra 5 điểm đáng chú ý nhất, giải thích theo ngôn ngữ dễ hiểu.
            Trả lời theo bullet points, đúng 5 bullet points
            """
        )
    )
    human_question_message = HumanMessagePromptTemplate.from_template("Câu hỏi: {question}")
    messages = [system_message, human_question_message]
    prompt = ChatPromptTemplate.from_messages(messages)

    def __init__(self, chat_model_service: ChatModelService):
        self.chat_model = chat_model_service.chat_model

    def __call__(self, state: TarotTellingState):
        self.prompt.extend([HumanMessage(content=a) for a in state["analysis"]])
        chain = self.prompt | self.chat_model
        summary: AIMessage = chain.invoke({"question": state["messages"][0].content})
        return TarotTellingState(message=[summary], summary=summary.content)
