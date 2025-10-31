import numpy as np
import casadi as ca

class _MTensor:

    def __init__(self, name, *shape):
        self._shape = tuple(shape)
        self._mx = ca.MX.sym(name, np.prod(shape))

    @property
    def shape(self):
        return self._shape

    def __getattr__(self, attr):
        return getattr(self._mx, attr)

    def __getitem__(self, k):
        assert len(k) == len(self._shape)
        return self._mx[np.ravel_multi_index(tuple(k), self._shape)]