from abc import ABC, abstractmethod


class ResumeServiceInterface(ABC):
    @abstractmethod
    async def tailor_resume(
        self,
        resume_text: str,
        job_description: str,
        tone: str = "professional"
    ) -> str:
        """Abstract method for resume tailoring"""
        pass
