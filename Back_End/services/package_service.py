"""
Package service layer for business logic.
"""

import logging
from sqlalchemy.orm import Session
from models.package import Package, PackageType
from schemas.package import PackageCreate, PackageUpdate

logger = logging.getLogger(__name__)


class PackageService:
    """Service for package operations."""

    @staticmethod
    def get_all_packages(db: Session, skip: int = 0, limit: int = 100) -> tuple[list[Package], int]:
        """Get all active packages."""
        packages = db.query(Package).filter(Package.active == 1).offset(skip).limit(limit).all()
        total = db.query(Package).filter(Package.active == 1).count()
        return packages, total

    @staticmethod
    def get_packages_by_type(db: Session, package_type: PackageType) -> list[Package]:
        """Get packages by type (hourly, weekly, monthly)."""
        return db.query(Package).filter(
            Package.package_type == package_type,
            Package.active == 1
        ).all()

    @staticmethod
    def get_package_by_id(db: Session, package_id: int) -> Package | None:
        """Get package by ID."""
        return db.query(Package).filter(Package.id == package_id).first()

    @staticmethod
    def create_package(db: Session, package: PackageCreate) -> Package:
        """Create a new package."""
        db_package = Package(**package.model_dump())
        db.add(db_package)
        db.commit()
        db.refresh(db_package)
        logger.info(f"Package created: {db_package.id} - {db_package.name}")
        return db_package

    @staticmethod
    def update_package(db: Session, package_id: int, package_update: PackageUpdate) -> Package | None:
        """Update a package."""
        db_package = PackageService.get_package_by_id(db, package_id)
        if not db_package:
            return None

        update_data = package_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_package, field, value)

        db.add(db_package)
        db.commit()
        db.refresh(db_package)
        logger.info(f"Package updated: {package_id}")
        return db_package

    @staticmethod
    def delete_package(db: Session, package_id: int) -> bool:
        """Soft delete a package by marking it inactive."""
        db_package = PackageService.get_package_by_id(db, package_id)
        if not db_package:
            return False

        db_package.active = 0
        db.add(db_package)
        db.commit()
        logger.info(f"Package deleted: {package_id}")
        return True
