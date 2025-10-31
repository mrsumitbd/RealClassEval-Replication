import json
from io import open
import os

class PathJoiner:
    """Load directory names from SETTINGS.json.

    Originally written by Baris Umog (https://www.kaggle.com/barisumog).

    Usage:
        # In SETTINGS.json, "data": "/path/to/data/".
        # To load "/path/to/data/targets.array" file to y:
        PATH = PathJoiner()
        y = load(PATH.data('targets.array'))
    """

    def __init__(self, filename='SETTINGS.json'):
        with open(filename) as file:
            self.subdirs = json.load(file)

    def __getattr__(self, attr):
        subdir = self.subdirs[attr]
        return lambda *dirs: os.path.join(subdir, *dirs)