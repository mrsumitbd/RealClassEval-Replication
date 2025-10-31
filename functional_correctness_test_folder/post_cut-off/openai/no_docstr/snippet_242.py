
import sys


class ImmediateFlushSink:
    def __init__(self, stream=None):
        # Default to sys.stdout if no stream is provided
        self.stream = stream or sys.stdout

    def write(self, message):
        # Write the message to the stream and flush immediately
        self.stream.write(message)
        self.flush()

    def flush(self):
        # Flush the underlying stream if it supports flushing
        try:
            self.stream.flush()
        except AttributeError:
            # Some streams may not have a flush method; ignore in that case
            pass
