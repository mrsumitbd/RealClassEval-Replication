
class PrintAndFlushSink:

    def write(self, message: str):
        print(message, flush=True)

    def flush(self):
        '''Flush the stream.
        Already flushed on every write call.
        '''
        pass
