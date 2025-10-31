
class PrintAndFlushSink:

    def write(self, message: str):
        """Writes the given message to the standard output and immediately flushes the buffer."""
        print(message, end='', flush=False)

    def flush(self):
        """Flushes the standard output buffer."""
        import sys
        sys.stdout.flush()
