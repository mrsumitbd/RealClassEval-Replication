import atomicwrites
from builtins import FileExistsError

class atomic_overwrite:
    """Atomically write, but don't complain if file already exists"""

    def __init__(self, *args, **kwargs):
        self.writer = atomicwrites.atomic_write(*args, overwrite=False, **kwargs)

    def __enter__(self):
        return self.writer.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            return self.writer.__exit__(exc_type, exc_val, exc_tb)
        except FileExistsError:
            pass