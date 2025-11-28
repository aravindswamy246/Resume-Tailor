from openai import OpenAI
import os
from dotenv import load_dotenv


def get_openai_client():
    """
    Create and configure OpenAI client with API key from environment.
    Returns:
        OpenAI: Configured OpenAI client instance
    Raises:
        ValueError: If API key is not found in environment
    """
    load_dotenv()

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    return OpenAI(api_key=api_key)
