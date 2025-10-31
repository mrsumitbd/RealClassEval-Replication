import os


class InGivenDirectory:

    def __init__(self, path=None):
        self.path = path
        self._old_cwd = None

    def __enter__(self):
        self._old_cwd = os.getcwd()
        if self.path is not None:
            target = os.path.abspath(os.path.expanduser(
                os.path.expandvars(str(self.path))))
            os.chdir(target)
        return self

    def __exit__(self, exc, value, tb):
        if self._old_cwd is not None:
            try:
                os.chdir(self._old_cwd)
            finally:
                self._old_cwd = None
        return False
