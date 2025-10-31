import numpy as np

class OpticalElement:

    def __init__(self):
        self.name = 'OpticalElement'
        self.type = 'undefined'
        self.normals = []
        self._hits = []
        self._hits_type = []
        self.cellids = []

    def n_at(self, wave_length):
        return self.ref_index

    @property
    def hits(self):
        """Ray coordinates hitting this element"""
        return np.array(self._hits)

    @property
    def hits_type(self):
        """Flag +1 if ray is entering, -1 if exiting"""
        return np.array(self._hits_type)