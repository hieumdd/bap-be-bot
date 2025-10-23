import pytest

from app.core.chat_model import ChatModelService
from app.ziwei.ziwei_graph import ZiweiGraphService


class TestZiwei:
    @pytest.fixture
    def question(self):
        return "1998-10-31 lúc 21h nam mạng"

    def test_graph(self, question: str, chat_model_service: ChatModelService):
        ziwei_graph_service = ZiweiGraphService(chat_model_service)
        for node, state in ziwei_graph_service.run(question):
            print(f">>> {node}")
            print(state)
