"""
Payment service layer for M-Pesa integration and payment processing.
"""

import logging
from datetime import datetime
from sqlalchemy.orm import Session
from models.payment import Payment, PaymentStatus, PaymentMethod
from schemas.payment import PaymentCreate

logger = logging.getLogger(__name__)


class PaymentService:
    """Service for payment operations."""

    @staticmethod
    def create_payment(db: Session, payment: PaymentCreate) -> Payment:
        """Create a payment record."""
        db_payment = Payment(
            session_id=payment.session_id,
            phone=payment.phone,
            amount=payment.amount,
            method=payment.method,
            status=PaymentStatus.PENDING,
        )
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        logger.info(f"Payment created: {db_payment.id} for {payment.phone} - {payment.amount} KES")
        return db_payment

    @staticmethod
    def get_payment_by_id(db: Session, payment_id: int) -> Payment | None:
        """Get payment by ID."""
        return db.query(Payment).filter(Payment.id == payment_id).first()

    @staticmethod
    def get_payment_by_session(db: Session, session_id: int) -> Payment | None:
        """Get payment by session ID."""
        return db.query(Payment).filter(Payment.session_id == session_id).first()

    @staticmethod
    def get_payment_by_mpesa_receipt(db: Session, mpesa_receipt: str) -> Payment | None:
        """Get payment by M-Pesa receipt number (prevent duplicates)."""
        return db.query(Payment).filter(Payment.mpesa_receipt == mpesa_receipt).first()

    @staticmethod
    def verify_mpesa_payment(mpesa_receipt: str, amount: float, phone: str) -> bool:
        """
        Verify M-Pesa payment with M-Pesa API.
        
        In production, this would integrate with M-Pesa Daraja API.
        For now, this is a placeholder that should be implemented with actual API calls.
        """
        # TODO: Implement M-Pesa Daraja API integration
        # This should:
        # 1. Call M-Pesa API to verify transaction
        # 2. Validate amount and phone number
        # 3. Return True if verified, False otherwise
        
        logger.info(f"M-Pesa verification (placeholder): {mpesa_receipt} - {amount} KES from {phone}")
        return True

    @staticmethod
    def confirm_payment(db: Session, payment_id: int, mpesa_receipt: str) -> Payment | None:
        """
        Confirm a payment after M-Pesa verification.
        """
        db_payment = PaymentService.get_payment_by_id(db, payment_id)
        if not db_payment:
            return None

        # Check for duplicate M-Pesa receipt
        existing_payment = PaymentService.get_payment_by_mpesa_receipt(db, mpesa_receipt)
        if existing_payment:
            logger.warning(f"Duplicate M-Pesa receipt detected: {mpesa_receipt}")
            return None

        db_payment.mpesa_receipt = mpesa_receipt
        db_payment.status = PaymentStatus.COMPLETED
        db_payment.updated_at = datetime.utcnow()
        
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        logger.info(f"Payment confirmed: {payment_id} with receipt {mpesa_receipt}")
        return db_payment

    @staticmethod
    def fail_payment(db: Session, payment_id: int, reason: str = "") -> Payment | None:
        """Mark a payment as failed."""
        db_payment = PaymentService.get_payment_by_id(db, payment_id)
        if not db_payment:
            return None

        db_payment.status = PaymentStatus.FAILED
        db_payment.updated_at = datetime.utcnow()
        
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        logger.info(f"Payment failed: {payment_id} - {reason}")
        return db_payment

    @staticmethod
    def get_user_payment_history(db: Session, phone: str, limit: int = 10) -> list[Payment]:
        """Get payment history for a phone number."""
        return db.query(Payment).filter(Payment.phone == phone).order_by(
            Payment.created_at.desc()
        ).limit(limit).all()
