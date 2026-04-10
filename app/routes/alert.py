"""
app/routes/alert.py
-------------------
POST /alert  — standalone alert endpoint.
"""

from fastapi import APIRouter
from app.schemas.schemas import AlertInput

router = APIRouter(prefix="/alert", tags=["Alert"])


@router.post("/", summary="Trigger alert based on risk label")
def send_alert(body: AlertInput):
    if body.risk.upper() == "HIGH":
        return {"alert": "⚠️ HIGH RISK! Immediate action required!"}
    return {"alert": "✅ No alert triggered — risk is LOW."}