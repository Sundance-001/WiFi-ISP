"""
Payment and Voucher models for M-Pesa integration.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from database import Base


class PaymentStatus(str, enum.Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentMethod(str, enum.Enum):
    """Payment method enumeration."""
    MPESA = "mpesa"
    CREDIT_CARD = "credit_card"
    WALLET = "wallet"


class VoucherStatus(str, enum.Enum):
    """Voucher status enumeration."""
    ACTIVE = "active"
    REDEEMED = "redeemed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class Payment(Base):
    """
    Payment transaction for WiFi session.
    
    Attributes:
        id: Primary key
        session_id: Associated session ID
        phone: Customer phone number
        amount: Payment amount
        currency: Payment currency (KES for M-Pesa)
        method: Payment method
        mpesa_receipt: M-Pesa receipt number
        status: Payment status
        created_at: Payment timestamp
    """
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, index=True)
    phone = Column(String(20), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="KES", nullable=False)
    method = Column(SQLEnum(PaymentMethod), default=PaymentMethod.MPESA, nullable=False)
    mpesa_receipt = Column(String(100), unique=True, nullable=True)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    session = relationship("Session", back_populates="payment")


class Voucher(Base):
    """
    WiFi access voucher (complementary to payment).
    
    Attributes:
        id: Primary key
        code: Unique voucher code
        package_id: Associated package ID
        value: Voucher value/price
        status: Voucher status
        phone: Phone number this voucher is assigned to (if any)
        created_at: Voucher creation timestamp
        redeemed_at: Voucher redemption timestamp
        expires_at: Voucher expiration timestamp
    """
    __tablename__ = "vouchers"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    package_id = Column(Integer, ForeignKey("packages.id"), nullable=False)
    value = Column(Float, nullable=False)
    status = Column(SQLEnum(VoucherStatus), default=VoucherStatus.ACTIVE, nullable=False, index=True)
    phone = Column(String(20), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    redeemed_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=False)

    # Relationships
    package = relationship("Package")
