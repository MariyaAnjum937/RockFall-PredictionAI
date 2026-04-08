from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.models import SensorData
from app.schemas.schemas import SensorInput

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/data")
def store_data(data: SensorInput, db: Session = Depends(get_db)):
    sensor = SensorData(
        rainfall=data.rainfall,
        slope=data.slope,
        temperature=data.temperature
    )
    db.add(sensor)
    db.commit()
    return {"message": "Data stored successfully"}


@router.get("/data")
def get_data(db: Session = Depends(get_db)):
    data = db.query(SensorData).all()
    return data