import numpy as np

class Dataset:
    """Base class for datasets.

    The pre-processing step does nothing: attributes ``raw_data`` and ``data``
    point to the same object.
    """
    load_opts = {'delimiter': ','}

    def preprocess(self, raw_data, **kwargs):
        return raw_data

    def __init__(self, **kwargs):
        self.raw_data = np.loadtxt(get_path(self.file_name), **self.load_opts)
        self.data = self.preprocess(self.raw_data, **kwargs)