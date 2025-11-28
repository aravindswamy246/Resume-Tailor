from pydantic import BaseModel, Field


class ApiConfig(BaseModel):
    """API configuration settings"""
    max_request_size: int = Field(
        default=1024 * 1024,  # 1MB
        description="Maximum request size in bytes"
    )
    rate_limit: int = Field(
        default=60,
        description="Requests per minute"
    )
    timeout: int = Field(
        default=30,
        description="Request timeout in seconds"
    )


class OutputConfig(BaseModel):
    """Output configuration"""
    base_path: str = Field(
        default="data/output",
        description="Base path for output files"
    )
    file_prefix: str = Field(
        default="tailored_resume_",
        description="Prefix for output files"
    )
