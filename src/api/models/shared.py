from enum import Enum
from typing import Optional
from datetime import datetime


class ToneEnum(str, Enum):
    """Valid tone options for resume tailoring"""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    ACADEMIC = "academic"


class StatusEnum(str, Enum):
    """API status values"""
    SUCCESS = "success"
    ERROR = "error"
    PROCESSING = "processing"


class ApiMetadata:
    """Metadata for API responses"""
    processing_time: float
    timestamp: datetime = datetime.utcnow()
    request_id: str
    tokens_used: Optional[int] = None
