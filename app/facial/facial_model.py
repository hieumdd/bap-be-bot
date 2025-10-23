from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class FacialFeatures(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    gender: Annotated[str, Field(description="The portrait's gender")]
    forehead: Annotated[str, Field(description="The portrait's forehead")]
    eyebrows: Annotated[str, Field(description="The portrait's eyebrows")]
    eyes: Annotated[str, Field(description="The portrait's eyes")]
    nose: Annotated[str, Field(description="The portrait's nose")]
    mouth: Annotated[str, Field(description="The portrait's mouth")]
    chin: Annotated[str, Field(description="The portrait's chin")]
    ears: Annotated[str, Field(description="The portrait's ears")]
    complexion: Annotated[str, Field(description="The portrait's complexion")]

    error: Annotated[bool, Field(default=False, description="If error, set to True, else False")]


class FacialAnalysis(BaseModel):
    personality: Annotated[str, Field(description="Analyzed Personality")]
    career_fortune: Annotated[str, Field(description="Analyzed Career & Fortune")]
    love_life: Annotated[str, Field(description="Analyzed Love Life")]
    health: Annotated[str, Field(description="Analyzed Health")]
    summary: Annotated[str, Field(description="Analyzed Summary")]
