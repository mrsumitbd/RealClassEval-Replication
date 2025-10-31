import logging
from typing import Dict, Any, Optional
import logging.handlers

class LogContext:
    """Context manager for adding request context to logs."""

    def __init__(self, request_id: str, user_id: Optional[str]=None, ip_address: Optional[str]=None):
        self.request_id = request_id
        self.user_id = user_id
        self.ip_address = ip_address
        self.old_factory = None

    def __enter__(self):
        """Set up log context."""
        self.old_factory = logging.getLogRecordFactory()

        def context_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            record.request_id = self.request_id
            if self.user_id:
                record.user_id = self.user_id
            if self.ip_address:
                record.ip_address = self.ip_address
            return record
        logging.setLogRecordFactory(context_factory)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore original log factory."""
        logging.setLogRecordFactory(self.old_factory)