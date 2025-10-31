import arviz as az
from arviz.stats.stats_utils import _circular_standard_deviation, stats_variance_2d
import numpy as np

class Variance:
    params = (True, False)
    param_names = ('Numba',)

    def setup(self, numba_flag):
        self.data = np.random.rand(10000, 1000)
        if numba_flag:
            az.Numba.enable_numba()
        else:
            az.Numba.disable_numba()

    def time_variance_2d(self, numba_flag):
        stats_variance_2d(self.data)