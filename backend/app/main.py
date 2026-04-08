from fastapi import FastAPI
from app.database import engine, Base

from app.routes import predict, data, alert

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rockfall Prediction API")

app.include_router(predict.router)
app.include_router(data.router)
app.include_router(alert.router)