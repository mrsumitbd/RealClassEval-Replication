
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
            data = args[0]
            data = data.replace('\n', '')
            self.stream.write(data, **kwargs)
        else:
            self.stream.write(*args, **kwargs)

    def flush(self):
        '''
        Call the stream's flush method without any extra arguments.
        '''
        self.stream.flush()
