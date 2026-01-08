import pytest

from app.core.chat_model import ChatModelService
from app.ziwei.ziwei_graph import ZiweiGraphService


class TestZiwei:
    @pytest.fixture
    def ziwei_graph_service(self, chat_model_service: ChatModelService):
        return ZiweiGraphService(chat_model_service)

    @pytest.fixture
    def question(self):
        return "1998-10-31 lúc 21h nam mạng"

    def test_graph(self, ziwei_graph_service: ZiweiGraphService, question: str):
        for node, state in ziwei_graph_service.run(question):
            print(f">>> {node}")
            print(state)
