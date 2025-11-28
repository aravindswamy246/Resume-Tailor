import logging
from pathlib import Path
from datetime import datetime


class EnvMonitor:
    def __init__(self):
        log_dir = Path(__file__).parent.parent.parent / 'logs'
        log_dir.mkdir(exist_ok=True)

        logging.basicConfig(
            filename=log_dir / 'env_access.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('env_monitor')

    def log_access(self, file_path: Path):
        """Log each access to environment files."""
        self.logger.info(f"Environment accessed: {file_path}")
