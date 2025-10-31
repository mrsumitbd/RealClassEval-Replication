import numpy as np

class RatingsIterable:

    def __init__(self, path):
        self.file_paths = list(path.iterdir())

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, i):
        return np.load(self.file_paths[i])['arr_0']