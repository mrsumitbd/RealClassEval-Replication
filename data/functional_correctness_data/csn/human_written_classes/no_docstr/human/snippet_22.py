from os import chdir, path

class Directory:

    def __init__(self):
        self._old_path = path.dirname(path.abspath(__file__))
        self._new_path = path.dirname(self._old_path)

    def __enter__(self):
        chdir(self._new_path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        chdir(self._old_path)