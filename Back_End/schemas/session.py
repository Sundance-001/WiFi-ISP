"""
Pydantic schemas for Session model.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SessionCreate(BaseModel):
    """Schema for creating a session."""
    phone: str
    package_id: int
    device_id: Optional[int] = None
    duration_hours: int


class SessionUpdate(BaseModel):
    """Schema for updating a session."""
    data_used_mb: Optional[float] = None
    is_active: Optional[bool] = None


class SessionResponse(BaseModel):
    """Schema for session response."""
    id: int
    phone: str
    package_id: int
    device_id: Optional[int]
    session_token: str
    start_time: datetime
    end_time: datetime
    duration_hours: int
    data_used_mb: float
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SessionListResponse(BaseModel):
    """Schema for session list response."""
    total: int
    sessions: list[SessionResponse]
