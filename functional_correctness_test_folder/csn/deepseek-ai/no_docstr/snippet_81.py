
import os
from pathlib import Path


class ChDir:
    def __init__(self, dpath):
        self.dpath = dpath
        self.original_dir = None

    def __enter__(self):
        if self.dpath is not None:
            self.original_dir = os.getcwd()
            os.chdir(self.dpath)
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        if self.original_dir is not None:
            os.chdir(self.original_dir)
