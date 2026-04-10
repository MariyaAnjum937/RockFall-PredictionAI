from fastapi import APIRouter

router = APIRouter()

@router.post("/alert")
def send_alert(risk: str):
    if risk.upper() == "HIGH":
        return {"alert": "⚠️ HIGH RISK! Immediate action required!"}
    return {"alert": "No alert triggered"}