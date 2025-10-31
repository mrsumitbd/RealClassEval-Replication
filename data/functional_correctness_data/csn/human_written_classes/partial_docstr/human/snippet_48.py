import os
from pathlib import Path

class TempWorkDir:
    """Switches the working directory to be the one on which this file lives,
       while within the 'with' block.
    """

    def __init__(self, new=None):
        self.original = None
        self.new = new or str(Path(__file__).parent.resolve())

    def __enter__(self):
        self.original = str(Path('.').resolve())
        os.makedirs(self.new, exist_ok=True)
        os.chdir(self.new)
        return self

    def __exit__(self, *args):
        os.chdir(self.original)