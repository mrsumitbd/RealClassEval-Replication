import sys


class PrintAndFlushSink:

    def write(self, message: str):
        if not isinstance(message, str):
            message = str(message)
        sys.stdout.write(message)
        sys.stdout.flush()
        return len(message)

    def flush(self):
        '''Flush the stream.
        Already flushed on every write call.
        '''
        sys.stdout.flush()
