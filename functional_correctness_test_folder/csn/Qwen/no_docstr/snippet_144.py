
import os


class InGivenDirectory:

    def __init__(self, path=None):
        self.original_directory = os.getcwd()
        self.target_directory = path

    def __enter__(self):
        if self.target_directory:
            os.chdir(self.target_directory)
        return self

    def __exit__(self, exc, value, tb):
        os.chdir(self.original_directory)
