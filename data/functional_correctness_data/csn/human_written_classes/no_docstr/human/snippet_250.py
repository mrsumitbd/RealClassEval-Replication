import arviz as az
import numpy as np
from arviz.stats.density_utils import _fast_kde_2d, histogram, kde

class Kde_1d:
    params = [(True, False), (10 ** 5, 10 ** 6, 10 ** 7)]
    param_names = ('Numba', 'n')

    def setup(self, numba_flag, n):
        self.x = np.random.randn(n // 10, 10)
        if numba_flag:
            az.Numba.enable_numba()
        else:
            az.Numba.disable_numba()

    def time_fast_kde_normal(self, numba_flag, n):
        kde(self.x)