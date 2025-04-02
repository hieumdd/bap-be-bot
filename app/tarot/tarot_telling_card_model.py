from io import BytesIO

from pydantic import BaseModel, ConfigDict


class TarotTellingCard(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    is_reversed: bool
    meaning: str
    image: BytesIO
