import sys


class PrintAndFlushSink:

    def write(self, message: str):
        if message is None:
            message = ''
        print(message, end='')

    def flush(self):
        sys.stdout.flush()
