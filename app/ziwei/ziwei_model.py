import base64
from io import BytesIO
from typing import Annotated
from uuid import uuid4

from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, Field
from pydantic.json_schema import SkipJsonSchema
import requests


class ZiweiBirthchart(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    year: Annotated[int, Field(description="The user's birth year")]
    month: Annotated[int, Field(description="The user's birth month")]
    day: Annotated[int, Field(description="The user's birth day")]
    hour: Annotated[int, Field(description="The user's birth hour")]
    minute: Annotated[int, Field(description="The user's birth minute")]
    gender: Annotated[int, Field(description="The user's gender, Female is 0, Male is 1")]

    error: Annotated[bool, Field(default=False, description="If error, set to True, else False")]

    image_b64: Annotated[str | None, SkipJsonSchema(), Field(default=None)]
    image: Annotated[BytesIO | None, SkipJsonSchema(), Field(default=None)]

    def model_post_init(self, *args):
        if self.error:
            return
        response = requests.post(
            "https://tuvivietnam.vn/lasotuvi/ansaotuvi/",
            data={
                "ho_ten": str(uuid4()),
                "loai_lich": "duong",
                "anh_mau": "1",
                "gioi_tinh": str(self.gender),
                "nam_duong": str(self.year),
                "thang_duong": str(self.month),
                "ngay_duong": str(self.day),
                "gio_duong": str(self.hour),
                "phut_duong": str(self.minute),
            },
            headers={"Cache-Control": "no-cache"},
        )

        soup = BeautifulSoup(response.text, "html.parser")
        img_tag = soup.find("img", {"id": "aoc_result_img"})

        if not img_tag:
            raise Exception("Image tag not found in response")

        img = base64.b64decode(img_tag["src"].replace("data:image/jpeg;base64,", ""))
        self.image_b64 = img_tag["src"]
        self.image = BytesIO(img)


class ZiweiArcAnalysis(BaseModel):
    arc: str
    analysis: str
