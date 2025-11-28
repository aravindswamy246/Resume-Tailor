from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from .shared import StatusEnum
from enum import Enum


class ErrorDetail(BaseModel):
    """Detailed error information"""
    code: str
    message: str
    target: Optional[str] = None
    details: Optional[list[dict]] = None


class ApiError(BaseModel):
    """Standard API error response"""
    status: StatusEnum = StatusEnum.ERROR
    error: ErrorDetail
    correlation_id: Optional[str] = None
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat())


class ValidationError(ApiError):
    """Validation error specifics"""
    error: ErrorDetail = Field(
        default_factory=lambda: ErrorDetail(
            code="VALIDATION_ERROR",
            message="Request validation failed"
        )
    )


class ErrorCode(str, Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    TOKEN_LIMIT_EXCEEDED = "TOKEN_LIMIT_EXCEEDED"
    API_ERROR = "API_ERROR"
    FILE_SYSTEM_ERROR = "FILE_SYSTEM_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"


# Create an actual exception class
class DetailedApiException(Exception):
    """Base exception for detailed API errors"""

    def __init__(
        self,
        error_code: ErrorCode,
        message: str,
        correlation_id: Optional[str] = None,
        retry_after: Optional[int] = None,
        suggestion: Optional[str] = None
    ):
        self.error_code = error_code
        self.message = message
        self.correlation_id = correlation_id
        self.retry_after = retry_after
        self.suggestion = suggestion
        super().__init__(message)

    def to_response(self) -> 'DetailedApiError':
        """Convert exception to response model"""
        return DetailedApiError(
            error=ErrorDetail(
                code=self.error_code,
                message=self.message
            ),
            status=StatusEnum.ERROR,
            correlation_id=self.correlation_id,
            retry_after=self.retry_after,
            suggestion=self.suggestion
        )


class DetailedApiError(ApiError):
    """Enhanced error response model"""
    error: ErrorDetail
    retry_after: Optional[int] = None
    suggestion: Optional[str] = None
