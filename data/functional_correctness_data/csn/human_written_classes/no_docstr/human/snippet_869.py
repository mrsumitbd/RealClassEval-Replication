import os
from os import curdir, getenv, listdir, makedirs, sep, walk
import errno

class DirectoryMaker:

    def __init__(self, mode=None):
        self.mode = mode

    def make(self, path, recursive=False):
        makedir_args = [path]
        if self.mode is not None:
            makedir_args.append(self.mode)
        try:
            if recursive:
                makedirs(*makedir_args)
            else:
                os.mkdir(*makedir_args)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise