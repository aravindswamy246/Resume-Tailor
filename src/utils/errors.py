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

    def __str__(self):
        base_message = self.message
        if self.token_count and self.max_tokens:
            base_message += f" (got {self.token_count}, max allowed {self.max_tokens})"
        return base_message
