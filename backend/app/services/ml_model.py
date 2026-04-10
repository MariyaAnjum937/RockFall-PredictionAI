def predict_risk(rainfall: float, slope: float, temperature: float) -> str:
    # Simple rule-based logic (hackathon-friendly)

    if rainfall > 80 and slope > 45:
        return "HIGH"
    elif rainfall > 50 and slope > 30:
        return "MEDIUM"
    else:
        return "LOW"