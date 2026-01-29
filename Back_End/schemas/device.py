"""
Pydantic schemas for Device model.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DeviceCreate(BaseModel):
    """Schema for creating a device."""
    phone: str
    mac_address: str
    device_name: str
    device_type: str = "phone"
    is_primary: bool = True


class DeviceUpdate(BaseModel):
    """Schema for updating a device."""
    device_name: Optional[str] = None
    is_primary: Optional[bool] = None
    active: Optional[bool] = None


class DeviceResponse(BaseModel):
    """Schema for device response."""
    id: int
    phone: str
    mac_address: str
    device_name: str
    device_type: str
    is_primary: bool
    active: bool
    created_at: datetime
    last_used_at: datetime

    class Config:
        from_attributes = True


class DeviceListResponse(BaseModel):
    """Schema for device list response."""
    phone: str
    total: int
    devices: list[DeviceResponse]
