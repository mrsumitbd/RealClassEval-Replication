class ProgressBarStream:

    def __init__(self, stream):
        self.stream = stream
        self._in_progress_line = False

    def write(self, *args, **kwargs):
        s = ''.join(str(a) for a in args)
        if not s:
            return
        if self._in_progress_line and not s.startswith('\r'):
            self.stream.write('\n')
            self._in_progress_line = False
        self.stream.write(s)
        if '\n' in s:
            self._in_progress_line = False
        elif '\r' in s:
            self._in_progress_line = True

    def flush(self):
        flush = getattr(self.stream, 'flush', None)
        if callable(flush):
            flush()
