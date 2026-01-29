"""
Package model for WiFi ISP packages (hourly, weekly, monthly).
"""

from sqlalchemy import Column, Integer, String, Float, Enum as SQLEnum
import enum
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from database import Base


class PackageType(str, enum.Enum):
    """Package type enumeration."""
    HOURLY = "hourly"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class Package(Base):
    """
    WiFi ISP package offering.
    
    Attributes:
        id: Primary key
        name: Package name (e.g., "1 Hour", "5 Mbps Weekly")
        package_type: Type of package (hourly, weekly, monthly)
        duration_hours: Duration in hours (for hourly) or validity period
        speed_mbps: Speed tier in Mbps (for weekly/monthly)
        price: Package price
        description: Package description
    """
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    package_type = Column(SQLEnum(PackageType), nullable=False, index=True)
    duration_hours = Column(Integer, nullable=True)  # For hourly packages
    speed_mbps = Column(Integer, nullable=True)  # For weekly/monthly packages
    price = Column(Float, nullable=False)
    description = Column(String(512), nullable=True)
    active = Column(Integer, default=1)  # 1 = active, 0 = inactive
