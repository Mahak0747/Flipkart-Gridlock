"""Application startup — lightweight initialization (Render-safe)."""

from __future__ import annotations

import logging
from backend.core.config import DATA_DIR, PROJECT_ROOT
from backend.services.cache_service import DataCache

logger = logging.getLogger(__name__)


def run_startup() -> None:
    """
    Lightweight startup only.
    ❌ No ML model loading here (important for Render memory limit)
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("🚀 ParkWise AI backend starting")
    logger.info("Project root: %s", PROJECT_ROOT)

    # -----------------------------
    # SAFE: Cache initialization
    # -----------------------------
    try:
        DataCache.initialize()
        logger.info("✅ Cache initialized")
    except Exception as e:
        logger.warning("⚠️ Cache init skipped: %s", str(e))

    logger.info("✅ Startup complete (lightweight mode)")