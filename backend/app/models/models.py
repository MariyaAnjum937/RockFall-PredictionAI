from sqlalchemy import Column, Integer, Float, String
from app.database import Base

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    rainfall = Column(Float)
    slope = Column(Float)
    temperature = Column(Float)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    rainfall = Column(Float)
    slope = Column(Float)
    temperature = Column(Float)
    risk = Column(String)