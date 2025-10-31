import os

class WorkingDirectoryKeeper:
    """A context manager to get back the working directory as it was before.
    If you want to stack working directory keepers, you need a new instance
    for each stage.
    """
    active = False

    def __enter__(self):
        if self.active:
            raise RuntimeError('Already in a working directory keeper !')
        self.wd = os.getcwd()
        self.active = True

    def __exit__(self, *exc_args):
        os.chdir(self.wd)
        self.active = False