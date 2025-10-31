import numpy as np
from six.moves import xrange

class fun_qtt:

    def __init__(self, f, d, a, b, order='F'):
        self.f = f
        self.d = np.array(d, dtype=np.int32)
        self.m = self.d.size
        self.a = np.array(a)
        self.sz = 2 ** self.d
        self.h = (np.array(b) - self.a) / np.array(self.sz - 1, dtype=float)
        self.sm = np.zeros((self.m, self.d.sum()), dtype=np.int32)
        self.full_sz = np.array([2] * self.d.sum(), dtype=np.int32)
        self.order = order
        start = 0
        for i in xrange(self.m):
            for j in xrange(self.d[i]):
                self.sm[i, j + start] = 2 ** j
            start = start + self.d[i]

    def __call__(self, ind):
        if self.order is 'F':
            ind_tt = np.dot(self.sm, np.array(ind, dtype=np.int32) - 1)
        else:
            ind_tt = np.dot(self.sm, np.array(ind, dtype=np.int32))
        x = self.a + self.h * ind_tt
        return self.f(x)