"""
Packages router for WiFi ISP API.
Provides endpoints for managing and retrieving WiFi packages.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services.package_service import PackageService
from models.package import PackageType
from schemas.package import PackageListResponse, PackageResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Packages"],
)


@router.get("/packages", response_model=PackageListResponse)
async def get_packages(db: Session = Depends(get_db)):
    """
    Get all available WiFi packages.

    Returns:
        PackageListResponse: List of all active packages with count
    """
    packages, total = PackageService.get_all_packages(db)
    return {"total": total, "packages": packages}


@router.get("/packages/type/{package_type}", response_model=PackageListResponse)
async def get_packages_by_type(package_type: PackageType, db: Session = Depends(get_db)):
    """
    Get packages filtered by type (hourly, weekly, monthly).

    Args:
        package_type: The type of packages to retrieve

    Returns:
        PackageListResponse: List of packages of the specified type
    """
    packages = PackageService.get_packages_by_type(db, package_type)
    return {"total": len(packages), "packages": packages}


@router.get("/packages/{package_id}", response_model=PackageResponse)
async def get_package(package_id: int, db: Session = Depends(get_db)):
    """
    Get a specific package by ID.

    Args:
        package_id: The package ID

    Returns:
        PackageResponse: Package details

    Raises:
        HTTPException: 404 if package not found
    """
    package = PackageService.get_package_by_id(db, package_id)
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    return package
