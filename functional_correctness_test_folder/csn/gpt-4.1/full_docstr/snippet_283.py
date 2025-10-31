
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
        # Only process the first positional argument as the string to write
        s = args[0]
        # Remove trailing linebreaks (\n or \r\n)
        if isinstance(s, str):
            s = s.rstrip('\r\n')
        self.stream.write(s)
        # If there are more positional or keyword arguments, pass them (rare for write)
        # But for safety, if more args, pass them along (except the first, which we replaced)
        if len(args) > 1 or kwargs:
            self.stream.write(*args[1:], **kwargs)

    def flush(self):
        '''
        Call the stream's flush method without any extra arguments.
        '''
        self.stream.flush()
