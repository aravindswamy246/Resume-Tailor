import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
import uuid


class CustomLogger:
    """Custom logger with rotation capabilities"""

    def __init__(self,
                 name: str = "resume_tailor",
                 log_dir: str = None,
                 max_bytes: int = 10_000_000,  # 10MB
                 backup_count: int = 5):

        # Create logs directory if not specified
        if log_dir is None:
            log_dir = Path(__file__).parent.parent.parent / 'logs'

        log_dir = Path(log_dir)
        log_dir.mkdir(exist_ok=True)

        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Enhanced formatter with more details
        file_formatter = logging.Formatter(
            '%(asctime)s.%(msecs)03d - %(request_id)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )

        # File handler with rotation
        file_handler = RotatingFileHandler(
            log_dir / f"{name}.log",
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)

        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.request_id = None

    def set_request_context(self, request_id=None):
        """Set request context for the current operation"""
        self.request_id = request_id or str(uuid.uuid4())
        # Add request_id to logger's extra fields
        self.logger = logging.LoggerAdapter(
            self.logger,
            {'request_id': self.request_id}
        )

    def log_request(self, data: dict):
        """Log API request data with structured format"""
        request_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'request_id': self.request_id,
            'input_length': len(data.get('resume_text', '')) + len(data.get('job_description', '')),
            'tone': data.get('tone', 'professional'),
            'client_info': data.get('client_info', {}),
        }
        self.logger.info(f"Request: {request_data}")

    def log_response(self, data: dict):
        """Log API response data"""
        self.logger.info(f"Response sent: {data}")

    def log_error(self, error: Exception, context: dict = None):
        """Log error with context"""
        error_msg = f"Error occurred: {str(error)}"
        if context:
            error_msg += f" | Context: {context}"
        self.logger.error(error_msg, exc_info=True)

    def log_api_usage(self, response_data: dict):
        """Log OpenAI API usage statistics"""
        usage = response_data.get('usage', {})
        prompt_tokens = usage.get('prompt_tokens', 0)
        completion_tokens = usage.get('completion_tokens', 0)
        total_tokens = usage.get('total_tokens', 0)

        # Approximate cost calculation (adjust rates as needed)
        prompt_cost = (prompt_tokens * 0.0015) / 1000  # $0.0015 per 1k tokens
        completion_cost = (completion_tokens * 0.002) / \
            1000  # $0.002 per 1k tokens
        total_cost = prompt_cost + completion_cost

        self.logger.info(
            f"API Usage - Prompt Tokens: {prompt_tokens}, "
            f"Completion Tokens: {completion_tokens}, "
            f"Total Tokens: {total_tokens}, "
            f"Estimated Cost: ${total_cost:.4f}"
        )

    def cleanup_old_logs(self, max_days: int = 30):
        """Clean up log files older than max_days"""
        log_dir = Path(self.logger.handlers[0].baseFilename).parent
        current_time = datetime.now().timestamp()

        for log_file in log_dir.glob("*.log*"):
            file_age_days = (
                current_time - log_file.stat().st_mtime) / (24 * 3600)
            if file_age_days > max_days:
                log_file.unlink()
                self.logger.info(f"Removed old log file: {log_file.name}")

    def log_performance(self, start_time: float, end_time: float):
        """Log performance metrics"""
        duration = end_time - start_time
        self.logger.info(
            f"Performance - Total Duration: {duration:.2f}s, "
            f"Request ID: {self.request_id}"
        )
