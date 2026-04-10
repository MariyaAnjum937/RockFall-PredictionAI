from fastapi import FastAPI
from app.database import engine, Base

from app.routes.data import router as data_router
from app.routes.alert import router as alert_router
from app.routes.predict import router as predict_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(data_router)
app.include_router(alert_router)
app.include_router(predict_router)


@app.get("/")
def root():
    return {"message": "Rockfall API Running 🚀"}