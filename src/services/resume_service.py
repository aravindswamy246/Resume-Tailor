from .base import ResumeServiceInterface
from resume_tailor import ResumeTailor
from typing import Optional
import os


class ResumeService(ResumeServiceInterface):
    def __init__(self, tailor: Optional[ResumeTailor] = None):
        """
        Initialize service with optional ResumeTailor instance
        Allows dependency injection for testing and flexibility
        """
        self._tailor = tailor

    @property
    def tailor(self) -> ResumeTailor:
        """Lazy initialization of ResumeTailor if not injected"""
        if self._tailor is None:
            from utils.env_loader import load_environment

            load_environment()
            model = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')
            self._tailor = ResumeTailor(model=model)
        return self._tailor

    async def tailor_resume(
        self,
        resume_text: str,
        job_description: str,
        tone: str = "professional"
    ) -> dict:
        """
        Implementation of resume tailoring service
        Returns dict with 'content' and 'usage' keys
        """
        return await self.tailor.tailor_resume(
            resume_text=resume_text,
            job_description=job_description,
            tone=tone
        )
