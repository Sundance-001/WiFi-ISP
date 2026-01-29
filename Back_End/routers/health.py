"""
Health check router for WiFi ISP API.
Provides endpoints for monitoring API status and health.
"""

import logging
from datetime import datetime

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Health"],
)


@router.get("/health")
async def health_check():
    """
    Check API health status.

    Returns:
        dict: Health status, app name, version, and timestamp
    """
    return {
        "status": "healthy",
        "app": "WiFi ISP API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }
