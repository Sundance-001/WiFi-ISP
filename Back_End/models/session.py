"""
Session model for tracking active user WiFi sessions.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from database import Base


class Session(Base):
    """
    Active WiFi session for a user.
    
    Attributes:
        id: Primary key
        phone: User phone number
        package_id: Associated package ID
        device_id: Associated device ID
        session_token: Unique session token for authentication
        start_time: Session start timestamp
        end_time: Session expiry timestamp
        duration_hours: Total duration of the session
        data_used_mb: Data consumed in MB
        is_active: Whether session is currently active
    """
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), nullable=False, index=True)
    package_id = Column(Integer, ForeignKey("packages.id"), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=True)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration_hours = Column(Integer, nullable=False)
    data_used_mb = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    package = relationship("Package")
    device = relationship("Device", back_populates="sessions")
    payment = relationship("Payment", back_populates="session", uselist=False)
