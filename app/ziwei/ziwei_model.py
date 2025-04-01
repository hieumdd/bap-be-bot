from pydantic import BaseModel, Field


class ZiweiInput(BaseModel):
    """Always use this tool to structure your response to the user."""

    year: int = Field(description="The user's birth year")
    month: int = Field(description="The user's birth month")
    day: int = Field(description="The user's birth day")
    hour: int = Field(description="The user's birth hour")
    minute: int = Field(description="The user's birth minute")
    gender: int = Field(description="The user's gender, Female is 0, Male is 1")

    error: bool = Field(description="If error, set to True, else False")
