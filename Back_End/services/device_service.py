"""
Device service layer for managing user devices.
"""

import logging
from sqlalchemy.orm import Session
from models.device import Device
from schemas.device import DeviceCreate, DeviceUpdate

logger = logging.getLogger(__name__)


class DeviceService:
    """Service for device operations."""

    @staticmethod
    def get_device_by_id(db: Session, device_id: int) -> Device | None:
        """Get device by ID."""
        return db.query(Device).filter(Device.id == device_id).first()

    @staticmethod
    def get_devices_by_phone(db: Session, phone: str) -> list[Device]:
        """Get all devices for a phone number."""
        return db.query(Device).filter(Device.phone == phone).all()

    @staticmethod
    def get_device_by_mac(db: Session, mac_address: str) -> Device | None:
        """Get device by MAC address."""
        return db.query(Device).filter(Device.mac_address == mac_address).first()

    @staticmethod
    def create_device(db: Session, device: DeviceCreate) -> Device:
        """
        Create a new device.
        
        Enforces 2-device limit per phone number.
        If adding third device, deactivate oldest non-primary device.
        """
        # Check device limit
        existing_devices = DeviceService.get_devices_by_phone(db, device.phone)
        
        if len(existing_devices) >= 2:
            # Find and deactivate oldest non-primary device
            oldest_device = None
            for dev in existing_devices:
                if not dev.is_primary:
                    if oldest_device is None or dev.created_at < oldest_device.created_at:
                        oldest_device = dev
            
            if oldest_device:
                oldest_device.active = False
                db.add(oldest_device)
                logger.info(f"Device deactivated to maintain 2-device limit: {oldest_device.id}")
            else:
                # If all are primary, deactivate the oldest one
                oldest_device = min(existing_devices, key=lambda d: d.created_at)
                oldest_device.active = False
                db.add(oldest_device)
                logger.info(f"Device deactivated (all primary): {oldest_device.id}")

        # Create new device
        db_device = Device(**device.model_dump())
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        logger.info(f"Device created: {db_device.id} for {device.phone}")
        return db_device

    @staticmethod
    def update_device(db: Session, device_id: int, device_update: DeviceUpdate) -> Device | None:
        """Update device details."""
        db_device = DeviceService.get_device_by_id(db, device_id)
        if not db_device:
            return None

        update_data = device_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_device, field, value)

        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        logger.info(f"Device updated: {device_id}")
        return db_device

    @staticmethod
    def deactivate_device(db: Session, device_id: int) -> bool:
        """Deactivate a device."""
        db_device = DeviceService.get_device_by_id(db, device_id)
        if not db_device:
            return False

        db_device.active = False
        db.add(db_device)
        db.commit()
        logger.info(f"Device deactivated: {device_id}")
        return True

    @staticmethod
    def check_device_limit(db: Session, phone: str) -> tuple[bool, int]:
        """
        Check device limit for a phone number.
        Returns: (can_add_device, active_device_count)
        """
        devices = DeviceService.get_devices_by_phone(db, phone)
        active_devices = [d for d in devices if d.active]
        return len(active_devices) < 2, len(active_devices)
