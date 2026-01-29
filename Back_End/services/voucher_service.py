"""
Voucher service layer for voucher management and validation.
"""

import logging
import secrets
import string
from datetime import datetime
from sqlalchemy.orm import Session
from models.payment import Voucher, VoucherStatus
from schemas.payment import VoucherCreate, VoucherRedeem

logger = logging.getLogger(__name__)


class VoucherService:
    """Service for voucher operations."""

    @staticmethod
    def generate_voucher_code() -> str:
        """Generate a unique voucher code (10 alphanumeric characters)."""
        characters = string.ascii_uppercase + string.digits
        code = "".join(secrets.choice(characters) for _ in range(10))
        return f"WIFI{code}"

    @staticmethod
    def create_voucher(db: Session, voucher: VoucherCreate) -> Voucher:
        """Create a new voucher."""
        code = VoucherService.generate_voucher_code()
        
        db_voucher = Voucher(
            code=code,
            package_id=voucher.package_id,
            value=voucher.value,
            expires_at=voucher.expires_at,
            status=VoucherStatus.ACTIVE,
        )
        db.add(db_voucher)
        db.commit()
        db.refresh(db_voucher)
        logger.info(f"Voucher created: {code} - {voucher.value} KES")
        return db_voucher

    @staticmethod
    def get_voucher_by_code(db: Session, code: str) -> Voucher | None:
        """Get voucher by code."""
        return db.query(Voucher).filter(Voucher.code == code).first()

    @staticmethod
    def get_voucher_by_id(db: Session, voucher_id: int) -> Voucher | None:
        """Get voucher by ID."""
        return db.query(Voucher).filter(Voucher.id == voucher_id).first()

    @staticmethod
    def validate_voucher(db: Session, code: str) -> tuple[bool, str]:
        """
        Validate a voucher before redemption.
        Returns: (is_valid, message)
        """
        voucher = VoucherService.get_voucher_by_code(db, code)
        
        if not voucher:
            return False, "Voucher not found"
        
        if voucher.status != VoucherStatus.ACTIVE:
            return False, f"Voucher is {voucher.status.value}"
        
        if datetime.utcnow() > voucher.expires_at:
            voucher.status = VoucherStatus.EXPIRED
            db.add(voucher)
            db.commit()
            return False, "Voucher expired"
        
        return True, "Voucher valid"

    @staticmethod
    def redeem_voucher(db: Session, voucher_redeem: VoucherRedeem) -> tuple[Voucher | None, str]:
        """
        Redeem a voucher for a phone number.
        Returns: (voucher, message)
        """
        is_valid, message = VoucherService.validate_voucher(db, voucher_redeem.code)
        if not is_valid:
            return None, message

        voucher = VoucherService.get_voucher_by_code(db, voucher_redeem.code)
        
        # Check if voucher is already assigned to a different phone
        if voucher.phone and voucher.phone != voucher_redeem.phone:
            return None, "Voucher already assigned to another phone"

        voucher.phone = voucher_redeem.phone
        voucher.status = VoucherStatus.REDEEMED
        voucher.redeemed_at = datetime.utcnow()
        
        db.add(voucher)
        db.commit()
        db.refresh(voucher)
        logger.info(f"Voucher redeemed: {voucher.code} by {voucher_redeem.phone}")
        return voucher, "Voucher redeemed successfully"

    @staticmethod
    def get_user_vouchers(db: Session, phone: str) -> list[Voucher]:
        """Get all redeemed vouchers for a phone number."""
        return db.query(Voucher).filter(
            Voucher.phone == phone,
            Voucher.status == VoucherStatus.REDEEMED,
        ).all()

    @staticmethod
    def get_active_vouchers(db: Session, skip: int = 0, limit: int = 100) -> tuple[list[Voucher], int]:
        """Get all active vouchers (for admin panel)."""
        vouchers = db.query(Voucher).filter(
            Voucher.status == VoucherStatus.ACTIVE
        ).offset(skip).limit(limit).all()
        total = db.query(Voucher).filter(Voucher.status == VoucherStatus.ACTIVE).count()
        return vouchers, total

    @staticmethod
    def cancel_voucher(db: Session, voucher_id: int) -> Voucher | None:
        """Cancel a voucher."""
        voucher = VoucherService.get_voucher_by_id(db, voucher_id)
        if not voucher:
            return None

        if voucher.status == VoucherStatus.REDEEMED:
            return None  # Cannot cancel redeemed voucher

        voucher.status = VoucherStatus.CANCELLED
        db.add(voucher)
        db.commit()
        db.refresh(voucher)
        logger.info(f"Voucher cancelled: {voucher.code}")
        return voucher
