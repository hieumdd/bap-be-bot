from io import BytesIO

import requests

from app.bot.message import ImageMessage


class DonateService:
    def return_donation_message(
        self,
        template_id: str = "r2hzVWk",
        bank_id: str = "970436",
        account_number: str = "0301000356930",
        account_name: str = "QUY NGUOI NGHIEN SONG TINH CAM",
        amount: str = "1000000",
    ):
        url = f"https://api.vietqr.io/image/{bank_id}-{account_number}-{template_id}.png"
        with requests.get(url, params={"accountName": account_name, "amount": amount}, stream=True) as r:
            buffer = BytesIO(r.content)
        return ImageMessage(buffer)
