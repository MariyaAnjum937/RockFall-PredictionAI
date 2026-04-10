"""
app/models/models.py
--------------------
SQLAlchemy ORM table definitions.
"""

from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class SensorData(Base):
    """Raw sensor readings submitted to /data."""
    __tablename__ = "sensor_data"

    id            = Column(Integer, primary_key=True, index=True)
    latitude      = Column(Float,   nullable=False)
    longitude     = Column(Float,   nullable=False)
    slope_angle   = Column(Float,   nullable=False)
    rock_type     = Column(String,  nullable=False)
    rainfall      = Column(Float,   nullable=True)
    temperature   = Column(Float,   nullable=False)
    vibration     = Column(Float,   nullable=True)
    displacement  = Column(Float,   nullable=False)
    strain        = Column(Float,   nullable=True)
    pore_pressure = Column(Float,   nullable=True)
    elevation     = Column(Float,   nullable=False)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())


class Prediction(Base):
    """Model predictions stored alongside the input that produced them."""
    __tablename__ = "predictions"

    id               = Column(Integer, primary_key=True, index=True)
    latitude         = Column(Float,   nullable=False)
    longitude        = Column(Float,   nullable=False)
    slope_angle      = Column(Float,   nullable=False)
    rock_type        = Column(String,  nullable=False)
    rainfall         = Column(Float,   nullable=True)
    temperature      = Column(Float,   nullable=False)
    vibration        = Column(Float,   nullable=True)
    displacement     = Column(Float,   nullable=False)
    strain           = Column(Float,   nullable=True)
    pore_pressure    = Column(Float,   nullable=True)
    elevation        = Column(Float,   nullable=False)
    risk_label       = Column(String,  nullable=False)   # "HIGH" / "LOW"
    risk_score       = Column(Integer, nullable=False)   # 1 / 0
    confidence_low   = Column(Float,   nullable=False)
    confidence_high  = Column(Float,   nullable=False)
    created_at       = Column(DateTime(timezone=True), server_default=func.now())