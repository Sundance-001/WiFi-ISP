"""
Pydantic schemas for Payment and Voucher models.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.payment import PaymentStatus, PaymentMethod, VoucherStatus


class PaymentCreate(BaseModel):
    """Schema for creating a payment."""
    session_id: int
    phone: str
    amount: float
    method: PaymentMethod = PaymentMethod.MPESA


class PaymentResponse(BaseModel):
    """Schema for payment response."""
    id: int
    session_id: int
    phone: str
    amount: float
    currency: str
    method: PaymentMethod
    mpesa_receipt: Optional[str]
    status: PaymentStatus
    created_at: datetime

    class Config:
        from_attributes = True


class VoucherCreate(BaseModel):
    """Schema for creating a voucher."""
    package_id: int
    value: float
    expires_at: datetime


class VoucherRedeem(BaseModel):
    """Schema for redeeming a voucher."""
    code: str
    phone: str


class VoucherResponse(BaseModel):
    """Schema for voucher response."""
    id: int
    code: str
    package_id: int
    value: float
    status: VoucherStatus
    phone: Optional[str]
    created_at: datetime
    redeemed_at: Optional[datetime]
    expires_at: datetime

    class Config:
        from_attributes = True
