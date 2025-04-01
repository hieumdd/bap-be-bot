import base64
from io import BytesIO

from bs4 import BeautifulSoup
import requests

from app.ziwei.ziwei_model import ZiweiInput


def generate_ziwei_image(ziwei_input: ZiweiInput):
    response = requests.post(
        "https://tuvivietnam.vn/lasotuvi/ansaotuvi/",
        data={
            "ho_ten": "Eck Xiao Lunch Bot",
            "loai_lich": "duong",
            "anh_mau": "1",
            "gioi_tinh": str(ziwei_input.gender),
            "nam_duong": str(ziwei_input.year),
            "thang_duong": str(ziwei_input.month),
            "ngay_duong": str(ziwei_input.day),
            "gio_duong": str(ziwei_input.hour),
            "phut_duong": str(ziwei_input.minute),
        },
        headers={"Cache-Control": "no-cache"},
    )

    soup = BeautifulSoup(response.text, "html.parser")
    img_tag = soup.find("img", {"id": "aoc_result_img"})

    if not img_tag:
        raise Exception("Image tag not found in response")

    b64_img = img_tag["src"]
    img = base64.b64decode(b64_img.replace("data:image/jpeg;base64,", ""))

    return b64_img, BytesIO(img)
