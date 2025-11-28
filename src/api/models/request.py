from pydantic import BaseModel, Field, field_validator
from .shared import ToneEnum
import re


class TailorRequest(BaseModel):
    """
    Request model for resume tailoring with validation
    """
    resume_text: str = Field(
        ...,  # Required field
        min_length=100,
        max_length=5000,
        description="The resume text to be tailored"
    )

    job_description: str = Field(
        ...,
        min_length=50,
        max_length=2000,
        description="The job description to tailor against"
    )

    tone: ToneEnum = Field(
        default=ToneEnum.PROFESSIONAL,
        description="The tone to use in the tailored resume"
    )

    save_output: bool = Field(
        default=True,
        description="Whether to save the output to a file"
    )

    @field_validator('resume_text', 'job_description')
    def validate_text_content(cls, v):
        """Validate text doesn't contain harmful content"""
        # Remove any control characters
        v = re.sub(r'[\x00-\x1F\x7F]', '', v)

        # Check for minimum word count
        if len(v.split()) < 10:
            raise ValueError("Text must contain at least 10 words")

        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "resume_text": "Enter your resume content here, ensuring it has at least 10 words to pass validation.",
                "job_description": "Enter your job description here, ensuring it has at least 10 words to pass validation.",
                "tone": "professional",
                "save_output": True
            }
        }
    }
