import numpy as np

class fun_ind:

    def __init__(self, f, n, a, b, order='F'):
        self.f = f
        self.n = np.array(n, dtype=np.int32)
        self.d = self.n.size
        self.a = np.array(a)
        self.h = (np.array(b) - self.a) / np.array(self.n - 1, dtype=float)

    def __call__(self, ind):
        if self.order is 'F':
            x = self.a + self.h * (np.array(ind, dtype=np.int32) - 1)
        else:
            x = self.a + self.h * np.array(ind, dtype=np.int32)
        return self.f(x)