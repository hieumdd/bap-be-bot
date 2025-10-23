from pathlib import Path

import pytest

from app.core.chat_model import ChatModelService
from app.facial.facial_graph import FacialGraphService
from app.utils.image import ImageBytesToB64


class TestFacial:
    @pytest.fixture
    def image_url(self):
        path = Path(__file__).parent / "facial_test.png"
        with path.open("rb") as f:
            image_bytes = f.read()
            return ImageBytesToB64().dump(image_bytes)

    def test_graph(self, image_url: str, chat_model_service: ChatModelService):
        service = FacialGraphService(chat_model_service)
        for node, state in service.run(image_url):
            print(f">>> {node}")
            print(state)
