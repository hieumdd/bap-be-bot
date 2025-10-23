import pytest

from app.core.chat_model import ChatModelService
from app.tarot.tarot_graph import TarotGraphService


class TestTarot:
    @pytest.fixture
    def question(self):
        return "Tôi nên làm gì hôm nay"

    def test_graph(self, question: str, chat_model_service: ChatModelService):
        tarot_graph_service = TarotGraphService(chat_model_service)
        for node, state in tarot_graph_service.run(question):
            print(f">>> {node}")
            print(state)
