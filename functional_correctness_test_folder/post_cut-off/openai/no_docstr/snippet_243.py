class PrintAndFlushSink:
    def write(self, message: str):
        import sys
        sys.stdout.write(message)
        sys.stdout.flush()

    def flush(self):
        import sys
        sys.stdout.flush()
