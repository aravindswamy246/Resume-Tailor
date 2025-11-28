import os
from pathlib import Path
from dotenv import load_dotenv
from .env_monitor import EnvMonitor


def load_environment():
    """
    Load and validate environment variables with monitoring.
    Works with both .env files (local) and environment variables (Docker).

    Returns:
        bool: True if environment is properly configured
    Raises:
        ValueError: If required variables are missing
    """
    root_dir = Path(__file__).parent.parent.parent
    env_path = root_dir / '.env'

    # Load .env file if it exists (local development)
    if env_path.exists():
        # Monitor access
        monitor = EnvMonitor()
        monitor.log_access(env_path)

        # Load variables
        load_dotenv(env_path)

    # Handle API key mapping (support both variable names)
    api_key = os.getenv('OPENAI_API_KEY') or os.getenv('GPT_SECRET_KEY')
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key

    # Validate required variables
    required_vars = ['OPENAI_API_KEY']
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Set them in .env file (local) or pass via docker-compose (Docker)."
        )

    return True
