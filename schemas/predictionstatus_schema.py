
from pydantic import BaseModel

class PredictionStatusResponse(BaseModel):
    class_id: int
    has_prediction1: bool
    has_prediction2: bool
    has_prediction3: bool