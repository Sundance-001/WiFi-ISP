"""
Database seeding script - populate initial packages
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database import SessionLocal, Base, engine
from models.package import Package, PackageType
from services.package_service import PackageService

def seed_packages():
    """Seed the database with initial packages."""
    db = SessionLocal()
    
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created")
        
        # Check if packages already exist
        existing = db.query(Package).count()
        if existing > 0:
            print(f"✓ Database already has {existing} packages. Skipping seed.")
            return
        
        # Hourly packages
        hourly_plans = [
            Package(
                name="1 Hour",
                package_type=PackageType.HOURLY,
                duration_hours=1,
                price=0.50,
                description="1 hour of WiFi access",
                active=1
            ),
            Package(
                name="3 Hours",
                package_type=PackageType.HOURLY,
                duration_hours=3,
                price=1.25,
                description="3 hours of WiFi access",
                active=1
            ),
            Package(
                name="8 Hours",
                package_type=PackageType.HOURLY,
                duration_hours=8,
                price=2.50,
                description="8 hours of WiFi access",
                active=1
            ),
            Package(
                name="16 Hours",
                package_type=PackageType.HOURLY,
                duration_hours=16,
                price=4.00,
                description="16 hours of WiFi access",
                active=1
            ),
            Package(
                name="24 Hours",
                package_type=PackageType.HOURLY,
                duration_hours=24,
                price=6.00,
                description="24 hours of WiFi access",
                active=1
            ),
        ]
        
        # Weekly packages
        weekly_plans = [
            Package(
                name="5 Mbps - Weekly",
                package_type=PackageType.WEEKLY,
                speed_mbps=5,
                price=7.00,
                description="5 Mbps speed for 7 days",
                active=1
            ),
            Package(
                name="20 Mbps - Weekly",
                package_type=PackageType.WEEKLY,
                speed_mbps=20,
                price=12.00,
                description="20 Mbps speed for 7 days",
                active=1
            ),
            Package(
                name="100 Mbps - Weekly",
                package_type=PackageType.WEEKLY,
                speed_mbps=100,
                price=20.00,
                description="100 Mbps speed for 7 days",
                active=1
            ),
        ]
        
        # Monthly packages
        monthly_plans = [
            Package(
                name="5 Mbps - Monthly",
                package_type=PackageType.MONTHLY,
                speed_mbps=5,
                price=25.00,
                description="5 Mbps speed for 30 days",
                active=1
            ),
            Package(
                name="20 Mbps - Monthly",
                package_type=PackageType.MONTHLY,
                speed_mbps=20,
                price=45.00,
                description="20 Mbps speed for 30 days",
                active=1
            ),
            Package(
                name="100 Mbps - Monthly",
                package_type=PackageType.MONTHLY,
                speed_mbps=100,
                price=90.00,
                description="100 Mbps speed for 30 days",
                active=1
            ),
        ]
        
        # Add all packages
        all_packages = hourly_plans + weekly_plans + monthly_plans
        db.add_all(all_packages)
        db.commit()
        
        print(f"✓ Seeded {len(all_packages)} packages:")
        print(f"  - {len(hourly_plans)} hourly plans")
        print(f"  - {len(weekly_plans)} weekly plans")
        print(f"  - {len(monthly_plans)} monthly plans")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_packages()
