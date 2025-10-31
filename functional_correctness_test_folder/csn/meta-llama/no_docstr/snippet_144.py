
import os


class InGivenDirectory:

    def __init__(self, path=None):
        self.path = path
        self.original_path = None

    def __enter__(self):
        self.original_path = os.getcwd()
        if self.path is not None:
            os.chdir(self.path)
        return self

    def __exit__(self, exc, value, tb):
        os.chdir(self.original_path)
