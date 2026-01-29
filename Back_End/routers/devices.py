"""
Devices router for WiFi ISP API.
Provides endpoints for managing user devices.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services.device_service import DeviceService
from schemas.device import DeviceCreate, DeviceUpdate, DeviceResponse, DeviceListResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Devices"],
)


@router.post("/devices", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def register_device(device: DeviceCreate, db: Session = Depends(get_db)):
    """
    Register a new device for a user.

    Enforces 2-device limit per phone. When adding a 3rd device,
    the oldest non-primary device is deactivated.

    Args:
        device: Device registration data

    Returns:
        DeviceResponse: Registered device details
    """
    new_device = DeviceService.create_device(db, device)
    return new_device


@router.get("/devices/phone/{phone}", response_model=DeviceListResponse)
async def get_user_devices(phone: str, db: Session = Depends(get_db)):
    """
    Get all devices for a phone number.

    Args:
        phone: Customer phone number

    Returns:
        DeviceListResponse: List of devices for the user
    """
    devices = DeviceService.get_devices_by_phone(db, phone)
    return {"phone": phone, "total": len(devices), "devices": devices}


@router.get("/devices/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: int, db: Session = Depends(get_db)):
    """
    Get device details by ID.

    Args:
        device_id: The device ID

    Returns:
        DeviceResponse: Device details

    Raises:
        HTTPException: 404 if device not found
    """
    device = DeviceService.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    return device


@router.patch("/devices/{device_id}", response_model=DeviceResponse)
async def update_device(device_id: int, device_update: DeviceUpdate, db: Session = Depends(get_db)):
    """
    Update device details.

    Args:
        device_id: The device ID to update
        device_update: Fields to update

    Returns:
        DeviceResponse: Updated device details

    Raises:
        HTTPException: 404 if device not found
    """
    updated_device = DeviceService.update_device(db, device_id, device_update)
    if not updated_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    return updated_device


@router.post("/devices/{device_id}/deactivate")
async def deactivate_device(device_id: int, db: Session = Depends(get_db)):
    """
    Deactivate a device.

    Args:
        device_id: The device ID to deactivate

    Returns:
        dict: Success message

    Raises:
        HTTPException: 404 if device not found
    """
    success = DeviceService.deactivate_device(db, device_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    return {"message": "Device deactivated successfully"}


@router.get("/devices/phone/{phone}/limit")
async def check_device_limit(phone: str, db: Session = Depends(get_db)):
    """
    Check device limit for a phone number.

    Args:
        phone: Customer phone number

    Returns:
        dict: Whether user can add another device and current device count
    """
    can_add, count = DeviceService.check_device_limit(db, phone)
    return {
        "phone": phone,
        "can_add_device": can_add,
        "active_devices": count,
        "device_limit": 2
    }
