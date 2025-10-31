import sys
import tempfile
import os

class Input:
    """A context manager to abstract input file, files or stdin"""

    def __init__(self, options):
        self.files = []
        self._stdin = None
        for in_file in options.files:
            if in_file == sys.stdin:
                _stdin = tempfile.NamedTemporaryFile(mode='w', prefix='stdin', suffix='.c', delete=False)
                _stdin.write(in_file.read())
                in_file = _stdin
            self.files.append(in_file.name)
            in_file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, ecx_tb):
        if self._stdin:
            os.remove(self._stdin.name)
        return False