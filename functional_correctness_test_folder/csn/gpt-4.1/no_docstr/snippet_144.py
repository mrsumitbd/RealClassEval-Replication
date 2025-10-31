
import os


class InGivenDirectory:

    def __init__(self, path=None):
        self.new_path = path
        self.old_path = None

    def __enter__(self):
        self.old_path = os.getcwd()
        if self.new_path is not None:
            os.chdir(self.new_path)
        return self

    def __exit__(self, exc, value, tb):
        if self.old_path is not None:
            os.chdir(self.old_path)
