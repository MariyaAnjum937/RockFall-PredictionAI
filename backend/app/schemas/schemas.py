from pydantic import BaseModel

class SensorInput(BaseModel):
    rainfall: float
    slope: float
    temperature: float


class PredictionResponse(BaseModel):
    risk: str