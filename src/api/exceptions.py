# api/exceptions.py
from typing import Optional


class TokenLimitError(Exception):
    """Raised when the input text exceeds token limits"""

    def __init__(self, message: str = "Input text exceeds token limit",
                 token_count: Optional[int] = None,
                 max_tokens: Optional[int] = None):
        self.message = message
        self.token_count = token_count
        self.max_tokens = max_tokens
        super().__init__(self.message)


class APIRateLimitError(Exception):
    """Raised when API rate limits are exceeded"""

    def __init__(self, message: str = "API rate limit exceeded",
                 retry_after: Optional[int] = None):
        self.message = message
        self.retry_after = retry_after
        super().__init__(self.message)
