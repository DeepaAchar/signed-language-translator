from pydantic import BaseModel
from typing import List
class GestureRecognitionResponse(BaseModel):
    gestures: List[str]
    confidence: float