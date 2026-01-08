import pytest

from app.core.chat_model import ChatModelService
from app.tarot.tarot_graph import TarotGraphService


class TestTarot:
    @pytest.fixture
    def tarot_graph_service(self, chat_model_service: ChatModelService):
        return TarotGraphService(chat_model_service)

    @pytest.fixture
    def question(self):
        return "Tôi nên làm gì hôm nay"

    def test_graph(self, tarot_graph_service: TarotGraphService, question: str):
        for node, state in tarot_graph_service.run(question):
            print(f">>> {node}")
            print(state)
