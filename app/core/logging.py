import logging
import os
from logging.handlers import RotatingFileHandler
from app.core.config import settings
import re

def setup_logging():
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)

    # Create formatters
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File Handler
    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, 'customer_service.log'),
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(settings.LOG_LEVEL)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(settings.LOG_LEVEL)

    # Add handlers to root logger
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return PrivacyAwareLogger(root_logger)

class PrivacyAwareLogger:
    def __init__(self, logger):
        self.logger = logger

    def info(self, message: str, privacy_level: str = "LOW", **kwargs):
        self._log("INFO", message, privacy_level, **kwargs)

    def warning(self, message: str, privacy_level: str = "LOW", **kwargs):
        self._log("WARNING", message, privacy_level, **kwargs)

    def error(self, message: str, privacy_level: str = "LOW", **kwargs):
        self._log("ERROR", message, privacy_level, **kwargs)

    def _log(self, level: str, message: str, privacy_level: str, **kwargs):
        masked_kwargs = {k: self._mask_sensitive_data(v) for k, v in kwargs.items()}
        log_message = f"{message} [Privacy: {privacy_level}] {masked_kwargs}"
        getattr(self.logger, level.lower())(log_message)


    def _mask_sensitive_data(self, data):
        if isinstance(data, str):
            # Mask email addresses
            data = re.sub(r'([\w\.-]+)@([\w\.-]+)', '****@****', data)

            # Mask phone numbers (assuming a simple format like 1234567890, haven't included country codes)
            data = re.sub(r'\b\d{10}\b', '*' * 10, data)


        elif isinstance(data, dict):
            # Recursively mask dictionary values
            return {k: self._mask_sensitive_data(v) for k, v in data.items()}

        elif isinstance(data, list):
            # Recursively mask list items
            return [self._mask_sensitive_data(item) for item in data]

        return data

# Create a global instance of PrivacyAwareLogger
logger = setup_logging()