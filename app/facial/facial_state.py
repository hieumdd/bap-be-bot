from app.core.state import BotMessagesState
from app.facial.facial_model import FacialFeatures


class FacialTellingState(BotMessagesState):
    image_url: str
    facial_features: FacialFeatures
