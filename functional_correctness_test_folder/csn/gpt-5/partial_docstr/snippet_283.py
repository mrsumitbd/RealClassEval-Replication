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
            return 0
        s = ''.join(str(a) for a in args)
        if s.endswith('\r\n'):
            s = s[:-2]
        elif s.endswith('\n') or s.endswith('\r'):
            s = s[:-1]
        return self.stream.write(s)

    def flush(self):
        '''
        Call the stream's flush method without any extra arguments.
        '''
        return self.stream.flush()
