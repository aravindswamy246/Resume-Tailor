from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from .shared import StatusEnum


class TailorResponse(BaseModel):
    """Response model for the tailor endpoint"""
    status: StatusEnum = Field(
        default=StatusEnum.SUCCESS,
        description="The status of the request"
    )
    tailored_resume: str = Field(
        ...,
        description="The tailored resume text"
    )
    saved_to: Optional[str] = Field(
        None,
        description="Path where the result was saved"
    )
    metadata: dict = Field(
        default_factory=lambda: {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "processing_time": None,
            "tokens_used": None
        },
        description="Metadata about the request"
    )


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    version: str
    uptime: float
    message: Optional[str] = None
    dependencies: dict = Field(
        default_factory=lambda: {
            "openai": "healthy",
            "file_system": "ok"
        }
    )
