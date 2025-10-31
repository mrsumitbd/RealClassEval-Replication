class _SocketAdaptor:

    def __init__(self, io):
        self._file = io

    def makefile(self, *args, **kwargs):
        return self._file