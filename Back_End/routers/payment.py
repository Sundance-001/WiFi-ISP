"""
Payments and Vouchers router for WiFi ISP API.
Provides endpoints for payment processing and voucher management.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services.payment_service import PaymentService
from services.voucher_service import VoucherService
from services.session_service import SessionService
from schemas.payment import PaymentCreate, PaymentResponse, VoucherCreate, VoucherRedeem, VoucherResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Payments", "Vouchers"],
)


# ============================================================================
# PAYMENT ENDPOINTS
# ============================================================================

@router.post("/payments", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    """
    Create a payment record for a session.

    Args:
        payment: Payment creation data with session_id, phone, amount, method

    Returns:
        PaymentResponse: Created payment details with status (pending)

    Raises:
        HTTPException: 404 if session not found
    """
    # Verify session exists
    session = SessionService.get_session_by_id(db, payment.session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    new_payment = PaymentService.create_payment(db, payment)
    return new_payment


@router.get("/payments/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: int, db: Session = Depends(get_db)):
    """
    Get payment details by ID.

    Args:
        payment_id: The payment ID

    Returns:
        PaymentResponse: Payment details

    Raises:
        HTTPException: 404 if payment not found
    """
    payment = PaymentService.get_payment_by_id(db, payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment


@router.post("/payments/{payment_id}/confirm")
async def confirm_payment(payment_id: int, mpesa_receipt: str, db: Session = Depends(get_db)):
    """
    Confirm a payment after M-Pesa verification.

    Args:
        payment_id: The payment ID to confirm
        mpesa_receipt: M-Pesa receipt number

    Returns:
        PaymentResponse: Updated payment with status (completed)

    Raises:
        HTTPException: 404 if payment not found
        HTTPException: 409 if M-Pesa receipt already exists
    """
    # Check for duplicate receipt
    existing = PaymentService.get_payment_by_mpesa_receipt(db, mpesa_receipt)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="M-Pesa receipt already processed"
        )

    confirmed_payment = PaymentService.confirm_payment(db, payment_id, mpesa_receipt)
    if not confirmed_payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return confirmed_payment


@router.post("/payments/{payment_id}/fail")
async def fail_payment(payment_id: int, reason: str = "", db: Session = Depends(get_db)):
    """
    Mark a payment as failed.

    Args:
        payment_id: The payment ID to fail
        reason: Failure reason

    Returns:
        PaymentResponse: Updated payment with status (failed)

    Raises:
        HTTPException: 404 if payment not found
    """
    failed_payment = PaymentService.fail_payment(db, payment_id, reason)
    if not failed_payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return failed_payment


@router.get("/payments/phone/{phone}/history")
async def get_payment_history(phone: str, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get payment history for a phone number.

    Args:
        phone: Customer phone number
        limit: Maximum number of records to return

    Returns:
        dict: List of payments for the user
    """
    payments = PaymentService.get_user_payment_history(db, phone, limit)
    return {"phone": phone, "total": len(payments), "payments": payments}


# ============================================================================
# VOUCHER ENDPOINTS
# ============================================================================

@router.post("/vouchers", response_model=VoucherResponse, status_code=status.HTTP_201_CREATED)
async def create_voucher(voucher: VoucherCreate, db: Session = Depends(get_db)):
    """
    Create a new voucher (admin endpoint).

    Args:
        voucher: Voucher creation data with package_id, value, expires_at

    Returns:
        VoucherResponse: Created voucher with generated code
    """
    new_voucher = VoucherService.create_voucher(db, voucher)
    return new_voucher


@router.get("/vouchers/{voucher_code}")
async def validate_voucher(voucher_code: str, db: Session = Depends(get_db)):
    """
    Validate a voucher without redeeming it.

    Args:
        voucher_code: The voucher code to validate

    Returns:
        dict: Validation status and message
    """
    is_valid, message = VoucherService.validate_voucher(db, voucher_code)
    return {"code": voucher_code, "is_valid": is_valid, "message": message}


@router.post("/vouchers/redeem", response_model=VoucherResponse)
async def redeem_voucher(voucher_redeem: VoucherRedeem, db: Session = Depends(get_db)):
    """
    Redeem a voucher for a phone number.

    Args:
        voucher_redeem: Voucher code and phone number

    Returns:
        VoucherResponse: Redeemed voucher details

    Raises:
        HTTPException: 400 if voucher cannot be redeemed
    """
    voucher, message = VoucherService.redeem_voucher(db, voucher_redeem)
    if not voucher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    return voucher


@router.get("/vouchers/phone/{phone}/redeemed")
async def get_user_vouchers(phone: str, db: Session = Depends(get_db)):
    """
    Get all redeemed vouchers for a phone number.

    Args:
        phone: Customer phone number

    Returns:
        dict: List of redeemed vouchers
    """
    vouchers = VoucherService.get_user_vouchers(db, phone)
    return {"phone": phone, "total": len(vouchers), "vouchers": vouchers}


@router.get("/vouchers/active")
async def get_active_vouchers(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    Get all active vouchers (admin endpoint).

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        dict: List of active vouchers
    """
    vouchers, total = VoucherService.get_active_vouchers(db, skip, limit)
    return {"total": total, "vouchers": vouchers}


@router.delete("/vouchers/{voucher_id}")
async def cancel_voucher(voucher_id: int, db: Session = Depends(get_db)):
    """
    Cancel an active voucher (admin endpoint).

    Args:
        voucher_id: The voucher ID to cancel

    Returns:
        dict: Success message

    Raises:
        HTTPException: 404 if voucher not found
        HTTPException: 400 if voucher is redeemed
    """
    cancelled = VoucherService.cancel_voucher(db, voucher_id)
    if not cancelled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel redeemed voucher"
        )
    return {"message": "Voucher cancelled successfully"}
