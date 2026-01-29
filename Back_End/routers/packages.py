"""
Packages router for WiFi ISP API.
Provides endpoints for managing and retrieving WiFi packages.
"""

import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Packages"],
)


@router.get("/packages")
async def get_packages():
    """
    Get all available WiFi packages.

    Returns:
        dict: Available packages organized by type (hourly, weekly, monthly)
    """
    return {
        "packages": [
            {
                "id": "hourly",
                "name": "Hourly Plans",
                "description": "Pay by the hour",
                "plans": [
                    {"duration": "1 hour", "price": 0.50},
                    {"duration": "3 hours", "price": 1.25},
                    {"duration": "8 hours", "price": 2.50},
                    {"duration": "16 hours", "price": 4.00},
                    {"duration": "24 hours", "price": 6.00},
                ],
            },
            {
                "id": "weekly",
                "name": "Weekly Plans",
                "description": "7 days of access",
                "plans": [
                    {"speed": "5 Mbps", "price": 7},
                    {"speed": "20 Mbps", "price": 12},
                    {"speed": "100 Mbps", "price": 20},
                ],
            },
            {
                "id": "monthly",
                "name": "Monthly Plans",
                "description": "30 days of access",
                "plans": [
                    {"speed": "5 Mbps", "price": 25},
                    {"speed": "20 Mbps", "price": 45},
                    {"speed": "100 Mbps", "price": 90},
                ],
            },
        ]
    }
