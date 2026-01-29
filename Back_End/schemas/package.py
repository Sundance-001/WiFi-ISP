"""
Pydantic schemas for Package model.
"""

from pydantic import BaseModel
from typing import Optional
from models.package import PackageType


class PackageCreate(BaseModel):
    """Schema for creating a package."""
    name: str
    package_type: PackageType
    duration_hours: Optional[int] = None
    speed_mbps: Optional[int] = None
    price: float
    description: Optional[str] = None
    active: int = 1


class PackageUpdate(BaseModel):
    """Schema for updating a package."""
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    active: Optional[int] = None


class PackageResponse(BaseModel):
    """Schema for package response."""
    id: int
    name: str
    package_type: PackageType
    duration_hours: Optional[int]
    speed_mbps: Optional[int]
    price: float
    description: Optional[str]
    active: int

    class Config:
        from_attributes = True


class PackageListResponse(BaseModel):
    """Schema for package list response."""
    total: int
    packages: list[PackageResponse]
