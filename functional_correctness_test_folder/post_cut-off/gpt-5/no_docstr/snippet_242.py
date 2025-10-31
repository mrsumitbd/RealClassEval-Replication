import sys


class ImmediateFlushSink:

    def __init__(self, stream=None):
        self.stream = stream if stream is not None else sys.stdout

    def write(self, message):
        if message is None:
            message = ''
        try:
            written = self.stream.write(message)
        except TypeError:
            written = self.stream.write(str(message))
        self.flush()
        return written

    def flush(self):
        flush = getattr(self.stream, "flush", None)
        if callable(flush):
            try:
                flush()
            except Exception:
                pass
