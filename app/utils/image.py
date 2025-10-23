from base64 import b64encode
from dataclasses import dataclass


@dataclass
class ImageBytesToB64:
    format_: str = "png"

    def dump(self, image_bytes: bytearray):
        return f"data:image/jpeg;base64,{b64encode(image_bytes).decode()}"
