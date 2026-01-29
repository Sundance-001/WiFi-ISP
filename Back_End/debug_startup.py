#!/usr/bin/env python
"""Startup script to debug server initialization."""

import sys
import traceback

try:
    print("1. Importing database...")
    from database import Base, engine
    print("   ✓ Database imported")
    
    print("2. Importing models...")
    from models.package import Package
    from models.session import Session
    from models.payment import Payment, Voucher
    from models.device import Device
    print("   ✓ Models imported")
    
    print("3. Importing services...")
    from services.package_service import PackageService
    from services.session_service import SessionService
    from services.payment_service import PaymentService
    from services.voucher_service import VoucherService
    from services.device_service import DeviceService
    print("   ✓ Services imported")
    
    print("4. Importing routers...")
    from routers import health, packages, contact, session, device, payment
    print("   ✓ Routers imported")
    
    print("5. Starting server...")
    import main
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"Message: {str(e)}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
