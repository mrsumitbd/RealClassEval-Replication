
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
        if args:
            text = args[0]
            if text.endswith('\n'):
                text = text[:-1]
            args = (text,) + args[1:]
        self.stream.write(*args, **kwargs)

    def flush(self):
        '''
        Call the stream's flush method without any extra arguments.
        '''
        self.stream.flush()
