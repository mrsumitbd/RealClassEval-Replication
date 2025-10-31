import numpy as np

class LinearMap:

    def __init__(self, xsh=0.0, ysh=0.0, rot=0.0, scale=1.0):
        _theta = np.deg2rad(rot)
        _mrot = np.zeros(shape=(2, 2), dtype=np.float64)
        _mrot[0] = (np.cos(_theta), np.sin(_theta))
        _mrot[1] = (-np.sin(_theta), np.cos(_theta))
        self.transform = _mrot * scale
        self.offset = [[xsh], [ysh]]

    def forward(self, pixx, pixy):
        return np.dot(self.transform, [pixx, pixy]) + self.offset