"""
app/routes/data.py
------------------
POST /data  — store raw sensor readings (no prediction).
GET  /data  — retrieve all stored sensor readings.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.models import SensorData
from app.schemas.schemas import SensorInput

router = APIRouter(prefix="/data", tags=["Sensor Data"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", summary="Store sensor reading")
def store_data(data: SensorInput, db: Session = Depends(get_db)):
    sensor = SensorData(
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
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    return {"message": "Data stored successfully", "id": sensor.id}


@router.get("/", summary="List all sensor readings")
def get_data(db: Session = Depends(get_db)):
    return db.query(SensorData).order_by(SensorData.created_at.desc()).all()