class ProgressBarStream:
    '''
    OutputStream wrapper to remove default linebreak at line endings.
    '''

    def __init__(self, stream):
        '''
        Wrap the given stream.
        '''
        self._stream = stream

    def write(self, *args, **kwargs):
        '''
        Call the stream's write method without linebreaks at line endings.
        '''
        if not args:
            data = ''
        elif len(args) == 1:
            data = args[0]
        else:
            if all(isinstance(a, (bytes, bytearray)) for a in args):
                data = b''.join(args)
            else:
                data = ''.join(str(a) for a in args)

        if isinstance(data, (bytes, bytearray)):
            if data.endswith(b'\r\n'):
                data = data[:-2]
            elif data.endswith(b'\n'):
                data = data[:-1]
        else:
            if data.endswith('\r\n'):
                data = data[:-2]
            elif data.endswith('\n'):
                data = data[:-1]

        return self._stream.write(data)

    def flush(self):
        '''
        Call the stream's flush method without any extra arguments.
        '''
        return self._stream.flush()
