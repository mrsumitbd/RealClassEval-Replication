
class PrintAndFlushSink:

    def write(self, message: str):
        print(message, end='', flush=True)

    def flush(self):
        import sys
        sys.stdout.flush()
