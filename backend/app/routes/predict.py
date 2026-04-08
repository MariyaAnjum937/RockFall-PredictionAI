from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.schemas import SensorInput, PredictionResponse
from app.services.ml_model import predict_risk
from app.database import SessionLocal
from app.models.models import Prediction

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/predict", response_model=PredictionResponse)
def predict(data: SensorInput, db: Session = Depends(get_db)):
    risk = predict_risk(data.rainfall, data.slope, data.temperature)

    prediction = Prediction(
        rainfall=data.rainfall,
        slope=data.slope,
        temperature=data.temperature,
        risk=risk
    )

    db.add(prediction)
    db.commit()

    return {"risk": risk}