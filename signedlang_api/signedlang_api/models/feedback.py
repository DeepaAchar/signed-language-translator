from pydantic import BaseModel

class FeedbckRequest(BaseModel):
    endpoint: str
    rating: int
    comment: str