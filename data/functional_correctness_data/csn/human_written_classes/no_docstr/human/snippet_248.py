import numpy as np
from arviz.stats.density_utils import _fast_kde_2d, histogram, kde
import arviz as az

class Fast_KDE_2d:
    params = [(True, False), ((100, 10 ** 4), (10 ** 4, 100), (1000, 1000))]
    param_names = ('Numba', 'shape')

    def setup(self, numba_flag, shape):
        self.x = np.random.randn(*shape)
        self.y = np.random.randn(*shape)
        if numba_flag:
            az.Numba.enable_numba()
        else:
            az.Numba.disable_numba()

    def time_fast_kde_2d(self, numba_flag, shape):
        _fast_kde_2d(self.x, self.y)