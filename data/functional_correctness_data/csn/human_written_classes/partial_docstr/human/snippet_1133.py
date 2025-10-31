class _StreamToLogger:
    """Send all that enters the stream to log-function."""

    def __init__(self, log):
        self._log = log

    def write(self, message):
        message = message.strip()
        if message:
            self._log(message)

    def flush(self):
        pass