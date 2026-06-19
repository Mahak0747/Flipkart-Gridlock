"""Model inference wrappers — lazy-loaded singleton (Render-safe)."""

from __future__ import annotations

from typing import Any
import pandas as pd

from app_utils import (
    batch_predict,
    load_model,
    predict_severity,
)

from backend.core.config import MODEL_PKL_PATH, EXPECTED_BUNDLE_KEYS


class ModelRegistry:
    """
    Lazy singleton model loader.
    Model loads ONLY when first needed (NOT at startup).
    """

    _bundle: dict[str, Any] | None = None

    @classmethod
    def _load(cls) -> dict[str, Any]:
        """Internal safe loader (runs once)."""
        if cls._bundle is None:
            try:
                cls._bundle = load_model(str(MODEL_PKL_PATH))

                # Validate only on first load
                verify_model_metadata(cls._bundle)

                print("✅ ML model loaded successfully")

            except FileNotFoundError:
                raise RuntimeError(
                    f"model.pkl not found at: {MODEL_PKL_PATH}"
                )

        return cls._bundle

    @classmethod
    def get_bundle(cls) -> dict[str, Any]:
        """Public access point (lazy loads model)."""
        return cls._load()

    @classmethod
    def load(cls, pkl_path: str | None = None) -> dict[str, Any]:
        """Backward compatibility (do not use in startup)."""
        if cls._bundle is None:
            cls._bundle = load_model(str(pkl_path or MODEL_PKL_PATH))
            verify_model_metadata(cls._bundle)
        return cls._bundle

    @classmethod
    def is_loaded(cls) -> bool:
        return cls._bundle is not None


# -----------------------------
# VALIDATION
# -----------------------------
def verify_model_metadata(bundle: dict[str, Any]) -> None:
    """Validate model structure once after loading."""

    missing = EXPECTED_BUNDLE_KEYS - set(bundle.keys())
    if missing:
        raise ValueError(f"model.pkl missing keys: {sorted(missing)}")

    if len(bundle["feature_cols"]) != 16:
        raise ValueError("Expected 16 feature columns")

    if list(bundle["label_order"]) != ["Low", "Medium", "High", "Critical"]:
        raise ValueError("Invalid label order")

    if not hasattr(bundle["model"], "predict"):
        raise ValueError("Invalid ML model object")


# -----------------------------
# PREDICTION API
# -----------------------------
def run_predict(input_data: dict[str, Any]) -> dict[str, Any]:
    return predict_severity(input_data, ModelRegistry.get_bundle())


def run_batch_predict(df: pd.DataFrame) -> pd.DataFrame:
    return batch_predict(df, ModelRegistry.get_bundle())


__all__ = [
    "ModelRegistry",
    "run_predict",
    "run_batch_predict",
    "verify_model_metadata",
]