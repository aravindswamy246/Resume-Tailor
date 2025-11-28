import asyncio
from openai import AsyncOpenAI
from utils import get_openai_client, CustomLogger
import random

# Initialize OpenAI async client
client = AsyncOpenAI(api_key=get_openai_client().api_key)

# Initialize logger
logger = CustomLogger(__name__)

# OpenAI pricing (as of Nov 2024) - update these if prices change
PRICING = {
    "gpt-4": {"input": 0.03, "output": 0.06},  # per 1K tokens
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-4o": {"input": 0.0025, "output": 0.01},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    "gpt-4-32k": {"input": 0.06, "output": 0.12},
}


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate the cost of an API call based on token usage."""
    # Find pricing for the model (handle model variants)
    pricing = None
    for model_prefix, prices in PRICING.items():
        if model.startswith(model_prefix):
            pricing = prices
            break

    if not pricing:
        # Default to gpt-4 pricing if model not found
        pricing = PRICING["gpt-4"]

    input_cost = (input_tokens / 1000) * pricing["input"]
    output_cost = (output_tokens / 1000) * pricing["output"]
    total_cost = input_cost + output_cost

    return round(total_cost, 6)


class ResumeTailor:
    def __init__(self, model, tone='professional'):
        """Initialize with model name."""
        self.model = model
        self.client = client

    async def tailor_resume(self, resume_text: str, job_description: str, tone: str = 'professional'):
        """Core business logic for resume tailoring"""
        prompt = f'''
        Tailor the following resume to better fit the job description.
        Use a {tone} tone in the output.
        
        Resume: {resume_text}
        Job Description: {job_description}
        '''

        try:
            response = await self._retry_on_rate_limit(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system",
                        "content": "You are a professional resume tailoring assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            # Extract token usage
            usage = response.usage
            input_tokens = usage.prompt_tokens
            output_tokens = usage.completion_tokens
            total_tokens = usage.total_tokens

            # Calculate cost
            cost = calculate_cost(self.model, input_tokens, output_tokens)

            # Log the usage and cost
            logger.logger.info(
                f"OpenAI API Call - Model: {self.model}, "
                f"Input Tokens: {input_tokens}, "
                f"Output Tokens: {output_tokens}, "
                f"Total Tokens: {total_tokens}, "
                f"Cost: ${cost:.6f}"
            )

            # Return both the content and usage info
            result = response.choices[0].message.content.strip()
            return {
                "content": result,
                "usage": {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens,
                    "cost_usd": cost
                }
            }

        except Exception as e:
            logger.log_error(e, {"model": self.model})
            print(f"API call failed: {type(e).__name__}: {str(e)}")
            raise

    async def _retry_on_rate_limit(self, func, *args, max_retries=6, initial_delay=1.0, max_delay=60.0, **kwargs):
        """Async retry wrapper with exponential backoff."""
        for attempt in range(1, max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries:
                    raise

                backoff = min(max_delay, initial_delay * (2 ** (attempt - 1)))
                sleep_for = random.uniform(0, backoff)
                print(
                    f"Rate limit detected. Retry {attempt}/{max_retries} after {sleep_for:.2f}s...")
                await asyncio.sleep(sleep_for)
