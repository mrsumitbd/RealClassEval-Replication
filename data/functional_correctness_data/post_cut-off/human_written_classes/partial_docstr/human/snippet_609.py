class SecureErrorHandler:
    """Context manager for secure error handling"""

    def __init__(self, operation_context: str):
        self.context = operation_context

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            safe_message = sanitize_error_message(exc_val, self.context)
            raise type(exc_val)(safe_message) from None
        return False