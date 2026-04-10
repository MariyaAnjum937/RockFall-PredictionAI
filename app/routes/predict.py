"""
app/routes/predict.py
---------------------
POST /predict  — runs the ML model and persists the result.
GET  /predict  — returns all stored predictions.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.models import Prediction
from app.schemas.schemas import SensorInput, PredictionResponse
from app.services.ml_model import predict_risk

router = APIRouter(prefix="/predict", tags=["Prediction"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PredictionResponse, summary="Predict rockfall risk")
def run_prediction(data: SensorInput, db: Session = Depends(get_db)):
    """
    Accept sensor readings **plus GPS coordinates** and return a rockfall
    risk prediction from the trained ML model.

    - Coordinates are stored in the database but are **not** used as ML features.
    - The model uses the 9 geotechnical features to classify risk as HIGH / LOW.
    """
    try:
        result = predict_risk(
            latitude      = data.latitude,
            longitude     = data.longitude,
            slope_angle   = data.slope_angle,
            rock_type     = data.rock_type,
            rainfall      = data.rainfall,
            temperature   = data.temperature,
            vibration     = data.vibration,
            displacement  = data.displacement,
            strain        = data.strain,
            pore_pressure = data.pore_pressure,
            elevation     = data.elevation,
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        )

    # Persist prediction
    record = Prediction(
        latitude        = data.latitude,
        longitude       = data.longitude,
        slope_angle     = data.slope_angle,
        rock_type       = data.rock_type,
        rainfall        = data.rainfall,
        temperature     = data.temperature,
        vibration       = data.vibration,
        displacement    = data.displacement,
        strain          = data.strain,
        pore_pressure   = data.pore_pressure,
        elevation       = data.elevation,
        risk_label      = result["risk_label"],
        risk_score      = result["risk_score"],
        confidence_low  = result["confidence_low"],
        confidence_high = result["confidence_high"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    alert_msg = (
        "⚠️ HIGH RISK — Immediate action required!"
        if result["risk_label"] == "HIGH"
        else "✅ LOW RISK — No immediate action needed."
    )

    return PredictionResponse(
        **result,
        alert=alert_msg,
    )


@router.get("/", summary="List all predictions")
def list_predictions(db: Session = Depends(get_db)):
    """Return all stored prediction records, newest first."""
    return db.query(Prediction).order_by(Prediction.created_at.desc()).all()