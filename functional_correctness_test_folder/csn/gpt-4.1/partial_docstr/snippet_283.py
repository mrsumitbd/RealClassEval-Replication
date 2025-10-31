
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
        text = args[0]
        # Remove trailing linebreaks
        if isinstance(text, str):
            text = text.rstrip('\r\n')
        self.stream.write(text, *args[1:], **kwargs)

    def flush(self):
        '''
        Call the stream's flush method without any extra arguments.
        '''
        self.stream.flush()
