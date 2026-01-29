"""
Session service layer for managing WiFi sessions.
"""

import logging
import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.session import Session as SessionModel
from models.device import Device
from schemas.session import SessionCreate, SessionUpdate

logger = logging.getLogger(__name__)


class SessionService:
    """Service for session operations."""

    @staticmethod
    def generate_session_token() -> str:
        """Generate a unique session token."""
        return secrets.token_urlsafe(32)

    @staticmethod
    def create_session(db: Session, session_data: SessionCreate) -> SessionModel:
        """Create a new WiFi session."""
        session_token = SessionService.generate_session_token()
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(hours=session_data.duration_hours)

        db_session = SessionModel(
            phone=session_data.phone,
            package_id=session_data.package_id,
            device_id=session_data.device_id,
            session_token=session_token,
            start_time=start_time,
            end_time=end_time,
            duration_hours=session_data.duration_hours,
            is_active=True,
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        logger.info(f"Session created: {db_session.id} for {session_data.phone}")
        return db_session

    @staticmethod
    def get_session_by_token(db: Session, session_token: str) -> SessionModel | None:
        """Get session by token."""
        return db.query(SessionModel).filter(SessionModel.session_token == session_token).first()

    @staticmethod
    def get_active_sessions(db: Session, phone: str) -> list[SessionModel]:
        """Get all active sessions for a phone number."""
        now = datetime.utcnow()
        return db.query(SessionModel).filter(
            SessionModel.phone == phone,
            SessionModel.is_active == True,
            SessionModel.end_time > now,
        ).all()

    @staticmethod
    def get_session_by_id(db: Session, session_id: int) -> SessionModel | None:
        """Get session by ID."""
        return db.query(SessionModel).filter(SessionModel.id == session_id).first()

    @staticmethod
    def update_session(db: Session, session_id: int, session_update: SessionUpdate) -> SessionModel | None:
        """Update session data."""
        db_session = SessionService.get_session_by_id(db, session_id)
        if not db_session:
            return None

        update_data = session_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_session, field, value)

        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session

    @staticmethod
    def expire_session(db: Session, session_id: int) -> bool:
        """Mark session as inactive."""
        db_session = SessionService.get_session_by_id(db, session_id)
        if not db_session:
            return False

        db_session.is_active = False
        db.add(db_session)
        db.commit()
        logger.info(f"Session expired: {session_id}")
        return True

    @staticmethod
    def check_session_validity(db: Session, session_token: str) -> tuple[bool, str]:
        """
        Check if a session is valid and still active.
        Returns: (is_valid, message)
        """
        db_session = SessionService.get_session_by_token(db, session_token)
        if not db_session:
            return False, "Session not found"

        if not db_session.is_active:
            return False, "Session is inactive"

        if datetime.utcnow() > db_session.end_time:
            db_session.is_active = False
            db.add(db_session)
            db.commit()
            return False, "Session expired"

        return True, "Session valid"
