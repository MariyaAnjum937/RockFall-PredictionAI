"""
app/services/ml_model.py
------------------------
Loads the trained model artefacts once at startup and exposes a single
`predict_risk(input_data)` function that the /predict route calls.
"""

import os
import numpy as np
import pandas as pd
import joblib

# ── Paths ─────────────────────────────────────────────────────────────────────
_ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "artifacts")

# ── Canonical feature order (must match training) ─────────────────────────────
FEATURE_COLUMNS = [
    "slope_angle",
    "rock_type",
    "rainfall",
    "temperature",
    "vibration",
    "displacement",
    "strain",
    "pore_pressure",
    "elevation",
]


def _load(filename):
    path = os.path.join(_ARTIFACTS_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Artifact not found: {path}\n"
            "Run  python -m ml.train  to train and save the model first."
        )
    return joblib.load(path)


# ── Lazy-loaded singletons (loaded once per worker process) ───────────────────
_model   = None
_scaler  = None
_imputer = None
_le      = None


def _ensure_loaded():
    global _model, _scaler, _imputer, _le
    if _model is None:
        _model   = _load("model.joblib")
        _scaler  = _load("scaler.joblib")
        _imputer = _load("imputer.joblib")
        _le      = _load("label_encoder.joblib")


# ── Public API ────────────────────────────────────────────────────────────────

def predict_risk(
    latitude: float,
    longitude: float,
    slope_angle: float,
    rock_type: str,
    rainfall: float,
    temperature: float,
    vibration: float,
    displacement: float,
    strain: float,
    pore_pressure: float,
    elevation: float,
) -> dict:
    """
    Run inference for a single location.

    Parameters
    ----------
    latitude, longitude : float
        GPS coordinates (stored in the DB; not used as model features).
    slope_angle         : degrees
    rock_type           : one of granite | limestone | shale | sandstone | basalt
    rainfall            : mm/day
    temperature         : °C
    vibration           : mm/s
    displacement        : mm
    strain              : dimensionless (0.0001 – 0.05)
    pore_pressure       : kPa
    elevation           : metres ASL

    Returns
    -------
    dict with keys: risk_label, risk_score, confidence_low, confidence_high
    """
    _ensure_loaded()

    # 1. Build a single-row DataFrame in the canonical feature order
    row = pd.DataFrame([{
        "slope_angle":   slope_angle,
        "rock_type":     rock_type,
        "rainfall":      rainfall,
        "temperature":   temperature,
        "vibration":     vibration,
        "displacement":  displacement,
        "strain":        strain,
        "pore_pressure": pore_pressure,
        "elevation":     elevation,
    }])[FEATURE_COLUMNS]

    # 2. Encode rock_type — handle unseen labels gracefully
    known_classes = list(_le.classes_)
    if rock_type not in known_classes:
        # Fall back to the most common class (granite)
        row["rock_type"] = _le.transform(["granite"])[0]
    else:
        row["rock_type"] = _le.transform([rock_type])[0]

    # 3. Impute any NaNs
    X_imputed = _imputer.transform(row)

    # 4. Scale
    X_scaled = _scaler.transform(X_imputed)

    # 5. Predict
    prediction  = int(_model.predict(X_scaled)[0])
    probability = _model.predict_proba(X_scaled)[0]

    return {
        "risk_label":       "HIGH" if prediction == 1 else "LOW",
        "risk_score":       prediction,
        "confidence_low":   round(float(probability[0]), 4),
        "confidence_high":  round(float(probability[1]), 4),
        "latitude":         latitude,
        "longitude":        longitude,
    }