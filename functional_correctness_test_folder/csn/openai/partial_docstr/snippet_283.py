class ProgressBarStream:
    '''
    OutputStream wrapper to remove default linebreak at line endings.
    '''

    def __init__(self, stream):
        self.stream = stream

    def write(self, *args, **kwargs):
        '''
        Call the stream's write method without linebreaks at line endings.
        '''
        if not args:
            return
        s = args[0]
        # Strip trailing newline characters if s is a string or bytes
        if isinstance(s, str):
            s = s.rstrip('\n')
        elif isinstance(s, bytes):
            s = s.rstrip(b'\n')
        # Call the underlying stream's write with the modified string
        return self.stream.write(s, *args[1:], **kwargs)

    def flush(self):
        '''
        Call the stream's flush method without any extra arguments.
        '''
        return self.stream.flush()
