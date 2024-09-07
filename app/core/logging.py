import logging
import re
from app.core.config import settings

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

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
        log_data = {
            "privacy_level": privacy_level,
            **{k: self._mask_sensitive_data(v) for k, v in kwargs.items()}
        }
        getattr(self.logger, level.lower())(f"{message} [Privacy: {privacy_level}]", extra=log_data)

    def _mask_sensitive_data(self, data):
        if isinstance(data, str):
            # Mask email addresses
            data = re.sub(r'([\w\.-]+)@([\w\.-]+)', '****@****', data)

            # Mask phone numbers (assuming a simple format like 1234567890, haven't include country codes)
            data = re.sub(r'\b\d{10}\b', '*' * 10, data)


        elif isinstance(data, dict):
            # Recursively mask dictionary values
            return {k: self._mask_sensitive_data(v) for k, v in data.items()}

        elif isinstance(data, list):
            # Recursively mask list items
            return [self._mask_sensitive_data(item) for item in data]

        return data

logger = PrivacyAwareLogger(logging.getLogger(settings.PROJECT_NAME))