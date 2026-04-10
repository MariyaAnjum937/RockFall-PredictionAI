# =============================================================================
# ROCKFALL RISK PREDICTION — ML TRAINING PIPELINE
# Saves trained model, scaler, imputer, and label-encoder to disk so the
# FastAPI backend can load them at startup.
# =============================================================================

import os
import numpy as np
import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
)
from sklearn.impute import SimpleImputer

try:
    from xgboost import XGBClassifier
    USE_XGBOOST = True
    print("✅ XGBoost available")
except ImportError:
    USE_XGBOOST = False
    print("⚠️  XGBoost not found — using GradientBoostingClassifier")

# Where to save artefacts (loaded by the FastAPI service)
ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "..", "app", "services", "artifacts")

# Canonical feature order — MUST match what the API sends
FEATURE_COLUMNS = [
    "slope_angle",
    "rock_type",      # encoded → integer
    "rainfall",
    "temperature",
    "vibration",
    "displacement",
    "strain",
    "pore_pressure",
    "elevation",
]


# =============================================================================
# 1. SYNTHETIC DATASET
# =============================================================================

def generate_synthetic_data(n_samples: int = 2000, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    slope_angle   = rng.uniform(15, 75, n_samples)
    rainfall      = rng.exponential(scale=30, size=n_samples)
    temperature   = rng.normal(loc=20, scale=8, size=n_samples)
    vibration     = rng.exponential(scale=0.5, size=n_samples)
    displacement  = rng.exponential(scale=2.0, size=n_samples)
    strain        = rng.uniform(0.0001, 0.05, n_samples)
    pore_pressure = rng.uniform(0, 500, n_samples)
    elevation     = rng.uniform(200, 1200, n_samples)
    rock_types    = ["granite", "limestone", "shale", "sandstone", "basalt"]
    rock_type     = rng.choice(rock_types, size=n_samples)

    risk_score = (
        0.30 * (slope_angle   / 75)   +
        0.20 * (rainfall      / 150)  +
        0.15 * (displacement  / 20)   +
        0.15 * (pore_pressure / 500)  +
        0.10 * (vibration     / 5)    +
        0.10 * (strain        / 0.05)
    )
    rock_modifier = np.where(rock_type == "shale",     0.10,
                    np.where(rock_type == "limestone",  0.05,
                    np.where(rock_type == "granite",   -0.10, 0.0)))
    risk_score = np.clip(risk_score + rock_modifier, 0, 1)
    rockfall_risk = (risk_score > 0.50).astype(int)

    df = pd.DataFrame({
        "slope_angle":   slope_angle,
        "rock_type":     rock_type,
        "rainfall":      rainfall,
        "temperature":   temperature,
        "vibration":     vibration,
        "displacement":  displacement,
        "strain":        strain,
        "pore_pressure": pore_pressure,
        "elevation":     elevation,
        "rockfall_risk": rockfall_risk,
    })

    # Simulate ~5 % sensor dropouts
    for col in ["rainfall", "vibration", "pore_pressure", "strain"]:
        idx = rng.choice(n_samples, size=int(0.05 * n_samples), replace=False)
        df.loc[idx, col] = np.nan

    return df


# =============================================================================
# 2. PREPROCESSING
# =============================================================================

def preprocess_data(df: pd.DataFrame):
    X = df.drop(columns=["rockfall_risk"])[FEATURE_COLUMNS].copy()
    y = df["rockfall_risk"].values

    le = LabelEncoder()
    X["rock_type"] = le.fit_transform(X["rock_type"].astype(str))

    imputer = SimpleImputer(strategy="median")
    X_imputed = imputer.fit_transform(X)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)

    print(f"[Preprocessing] shape={X_scaled.shape} | "
          f"Low={int((y==0).sum())} High={int((y==1).sum())}")
    return X_scaled, y, le, imputer, scaler


# =============================================================================
# 3. MODEL BUILDING
# =============================================================================

def build_models(random_state: int = 42) -> dict:
    rf = RandomForestClassifier(
        n_estimators=300,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight="balanced",
        n_jobs=-1,
        random_state=random_state,
    )

    if USE_XGBOOST:
        boost = XGBClassifier(
            n_estimators=300, max_depth=6, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8,
            use_label_encoder=False, eval_metric="logloss",
            random_state=random_state,
        )
        boost_name = "XGBoost"
    else:
        boost = GradientBoostingClassifier(
            n_estimators=300, max_depth=5, learning_rate=0.05,
            subsample=0.8, random_state=random_state,
        )
        boost_name = "GradientBoosting"

    return {"Random Forest": rf, boost_name: boost}


# =============================================================================
# 4. TRAINING + EVALUATION
# =============================================================================

def train_evaluate(models, X_train, y_train, X_test, y_test) -> dict:
    results = {}
    for name, model in models.items():
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = cross_val_score(model, X_train, y_train,
                                    cv=cv, scoring="roc_auc", n_jobs=-1)
        model.fit(X_train, y_train)

        y_pred  = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        results[name] = {
            "model":   model,
            "cv_auc":  cv_scores.mean(),
            "accuracy": accuracy_score(y_test, y_pred),
            "f1":       f1_score(y_test, y_pred, zero_division=0),
            "roc_auc":  roc_auc_score(y_test, y_proba),
        }
        print(f"[{name}] CV-AUC={cv_scores.mean():.4f} | "
              f"Test-AUC={results[name]['roc_auc']:.4f} | "
              f"F1={results[name]['f1']:.4f}")
    return results


# =============================================================================
# 5. SAVE ARTIFACTS
# =============================================================================

def save_artifacts(best_model, scaler, imputer, le):
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    joblib.dump(best_model, os.path.join(ARTIFACTS_DIR, "model.joblib"))
    joblib.dump(scaler,     os.path.join(ARTIFACTS_DIR, "scaler.joblib"))
    joblib.dump(imputer,    os.path.join(ARTIFACTS_DIR, "imputer.joblib"))
    joblib.dump(le,         os.path.join(ARTIFACTS_DIR, "label_encoder.joblib"))
    print(f"\n✅ Artifacts saved to: {ARTIFACTS_DIR}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("  ROCKFALL RISK — TRAINING PIPELINE")
    print("=" * 60)

    df = generate_synthetic_data(n_samples=2000, random_state=42)
    X, y, le, imputer, scaler = preprocess_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42
    )

    models  = build_models()
    results = train_evaluate(models, X_train, y_train, X_test, y_test)

    best_name  = max(results, key=lambda n: results[n]["roc_auc"])
    best_model = results[best_name]["model"]
    print(f"\n🏆 Best model : {best_name} (ROC-AUC={results[best_name]['roc_auc']:.4f})")

    save_artifacts(best_model, scaler, imputer, le)
    print("\n✅ Training complete.\n")


if __name__ == "__main__":
    main()