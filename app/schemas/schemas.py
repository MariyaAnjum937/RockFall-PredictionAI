"""
app/schemas/schemas.py
----------------------
Pydantic v2 schemas for request / response validation.
"""

from typing import Literal
from pydantic import BaseModel, Field


ROCK_TYPES = Literal["granite", "limestone", "shale", "sandstone", "basalt"]


class SensorInput(BaseModel):
    # ── Location ──────────────────────────────────────────────────────────────
    latitude:     float = Field(..., ge=-90,  le=90,   description="GPS latitude  (-90 to 90)")
    longitude:    float = Field(..., ge=-180, le=180,  description="GPS longitude (-180 to 180)")

    # ── ML features ──────────────────────────────────────────────────────────
    slope_angle:   float      = Field(..., ge=0,       le=90,    description="Slope angle in degrees")
    rock_type:     ROCK_TYPES = Field(...,                        description="Rock type at the location")
    rainfall:      float      = Field(..., ge=0,                  description="Rainfall in mm/day")
    temperature:   float      = Field(...,                        description="Temperature in °C")
    vibration:     float      = Field(..., ge=0,                  description="Vibration in mm/s")
    displacement:  float      = Field(..., ge=0,                  description="Ground displacement in mm")
    strain:        float      = Field(..., ge=0,       le=1,     description="Strain (dimensionless)")
    pore_pressure: float      = Field(..., ge=0,                  description="Pore water pressure in kPa")
    elevation:     float      = Field(...,                        description="Elevation in metres ASL")

    model_config = {
        "json_schema_extra": {
            "example": {
                "latitude":     28.6139,
                "longitude":    77.2090,
                "slope_angle":  52.0,
                "rock_type":    "shale",
                "rainfall":     85.0,
                "temperature":  28.0,
                "vibration":    1.2,
                "displacement": 5.5,
                "strain":       0.03,
                "pore_pressure":320.0,
                "elevation":    650.0,
            }
        }
    }


class PredictionResponse(BaseModel):
    risk_label:      str   = Field(..., description="'HIGH' or 'LOW'")
    risk_score:      int   = Field(..., description="Binary label: 1=HIGH, 0=LOW")
    confidence_low:  float = Field(..., description="Probability of LOW risk")
    confidence_high: float = Field(..., description="Probability of HIGH risk")
    latitude:        float
    longitude:       float
    alert:           str   = Field(..., description="Human-readable alert message")


class AlertInput(BaseModel):
    risk: str = Field(..., description="Risk label — 'HIGH' or 'LOW'")