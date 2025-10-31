class ProgressBarStream:
    '''
    OutputStream wrapper to remove default linebreak at line endings.
    '''

    def __init__(self, stream):
        '''
        Wrap the given stream.
        '''
        self.stream = stream

    def write(self, *args, **kwargs):
        '''
        Call the stream's write method without linebreaks at line endings.
        '''
        if not args:
            return
        # Only consider the first positional argument as the string to write
        s = args[0]
        # Strip trailing newline characters
        s = s.rstrip('\n')
        return self.stream.write(s, **kwargs)

    def flush(self):
        '''
        Call the stream's flush method without any extra arguments.
        '''
        return self.stream.flush()
