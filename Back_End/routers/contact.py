"""
Contact router for WiFi ISP API.
Provides endpoints for retrieving company contact information.
"""

import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Contact"],
)


@router.get("/contact")
async def get_contact_info():
    """
    Get company contact information.

    Returns:
        dict: Company contact details including phone, email, address, and website
    """
    return {
        "company": "WHi",
        "phone": "+1 555 555 5555",
        "email": "support@wifisp.example.com",
        "address": "123 Network Ave, City, State",
        "website": "https://wifisp.example.com",
    }
