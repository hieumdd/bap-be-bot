from pydantic import BaseModel, ConfigDict, Field


class Message(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    chat_id: int
    id: int
    timestamp: int
    text: str = Field(min_length=1)
    from_: str = Field(alias="from")
