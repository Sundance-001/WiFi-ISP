"""
Sessions router for WiFi ISP API.
Provides endpoints for managing WiFi sessions.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services.session_service import SessionService
from services.package_service import PackageService
from schemas.session import SessionCreate, SessionResponse, SessionListResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Sessions"],
)


@router.post("/sessions", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    """
    Create a new WiFi session.

    Args:
        session_data: Session creation data with phone, package_id, device_id, duration_hours

    Returns:
        SessionResponse: Created session details with token

    Raises:
        HTTPException: 404 if package not found
    """
    # Verify package exists
    package = PackageService.get_package_by_id(db, session_data.package_id)
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )

    new_session = SessionService.create_session(db, session_data)
    return new_session


@router.get("/sessions/phone/{phone}", response_model=SessionListResponse)
async def get_user_sessions(phone: str, db: Session = Depends(get_db)):
    """
    Get all active sessions for a phone number.

    Args:
        phone: Customer phone number

    Returns:
        SessionListResponse: List of active sessions
    """
    sessions = SessionService.get_active_sessions(db, phone)
    return {"total": len(sessions), "sessions": sessions}


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(session_id: int, db: Session = Depends(get_db)):
    """
    Get session details by ID.

    Args:
        session_id: The session ID

    Returns:
        SessionResponse: Session details

    Raises:
        HTTPException: 404 if session not found
    """
    session = SessionService.get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return session


@router.get("/sessions/token/{session_token}")
async def check_session_validity(session_token: str, db: Session = Depends(get_db)):
    """
    Check if a session token is valid.

    Args:
        session_token: The session token to validate

    Returns:
        dict: Validity status and message
    """
    is_valid, message = SessionService.check_session_validity(db, session_token)
    return {"is_valid": is_valid, "message": message}


@router.post("/sessions/{session_id}/end")
async def end_session(session_id: int, db: Session = Depends(get_db)):
    """
    End (expire) a WiFi session.

    Args:
        session_id: The session ID to end

    Returns:
        dict: Success message

    Raises:
        HTTPException: 404 if session not found
    """
    success = SessionService.expire_session(db, session_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return {"message": "Session ended successfully"}
