from pydantic import BaseModel

class SpeechToTextResponse(BaseModel):
    transcription: str