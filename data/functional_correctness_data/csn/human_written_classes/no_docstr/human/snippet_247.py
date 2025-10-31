from scipy.stats import circstd
from arviz.stats.stats_utils import _circular_standard_deviation, stats_variance_2d
import numpy as np

class CircStd:
    params = (True, False)
    param_names = ('Numba',)

    def setup(self, numba_flag):
        self.data = np.random.randn(10000, 1000)
        if numba_flag:
            self.circstd = _circular_standard_deviation
        else:
            self.circstd = circstd

    def time_circ_std(self, numba_flag):
        self.circstd(self.data)