from pydantic import BaseModel

class TextToSignRequest(BaseModel):
    text: str

class TextToSignResponse(BaseModel):
    videoUrl: str