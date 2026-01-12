import base64
from io import BytesIO
from typing import Annotated
from uuid import uuid4

from bs4 import BeautifulSoup
import pymupdf
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

    image_b64: Annotated[str | None, SkipJsonSchema(), Field(default=None, exclude=True)]
    image: Annotated[BytesIO | None, SkipJsonSchema(), Field(default=None, exclude=True)]

    def model_post_init(self, *args):
        if self.error:
            return

        with requests.post(
            "https://xem.tracuutuvi.com/",
            data={
                "full_name": str(uuid4()),
                "gender": str(self.gender),
                "lich": 1,
                "hour": str(self.hour),
                "minute": str(self.minute),
                "day": str(self.day),
                "month": str(self.month),
                "year": str(self.year),
            },
        ) as r:
            code_response = r.text
        soup = BeautifulSoup(code_response, features="html.parser")
        code = soup.find("div", {"id": "result-content"})["code"]

        with requests.get(f"https://xem.tracuutuvi.com/pdf/laso_pdf?c={code}") as r:
            pdf_buf = BytesIO(r.content)

        with pymupdf.open(stream=pdf_buf.getvalue(), filetype="pdf") as doc:
            pix = doc[0].get_pixmap(dpi=150)

        image_bytes = pix.tobytes("png")
        self.image_b64 = f"data:image/png;base64,{base64.b64encode(image_bytes).decode()}"
        self.image = BytesIO(image_bytes)


class ZiweiArcAnalysis(BaseModel):
    arc: str
    analysis: str
