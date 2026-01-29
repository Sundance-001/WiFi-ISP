"""
Device model for tracking user devices (1-2 per user).
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from database import Base


class Device(Base):
    """
    User device for WiFi access.
    
    Attributes:
        id: Primary key
        phone: User phone number (user identifier)
        mac_address: Device MAC address
        device_name: User-friendly device name
        device_type: Type of device (phone, laptop, tablet, etc.)
        is_primary: Whether this is the primary device
        active: Whether device is active
        created_at: Registration timestamp
        last_used_at: Last session timestamp
    """
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), nullable=False, index=True)
    mac_address = Column(String(17), unique=True, nullable=False, index=True)
    device_name = Column(String(100), nullable=False)
    device_type = Column(String(50), default="phone")  # phone, laptop, tablet
    is_primary = Column(Boolean, default=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sessions = relationship("Session", back_populates="device")
