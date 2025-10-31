import arviz as az
from arviz.stats.density_utils import _fast_kde_2d, histogram, kde
import numpy as np

class Hist:
    params = (True, False)
    param_names = ('Numba',)

    def setup(self, numba_flag):
        self.data = np.random.rand(10000, 1000)
        if numba_flag:
            az.Numba.enable_numba()
        else:
            az.Numba.disable_numba()

    def time_histogram(self, numba_flag):
        histogram(self.data, bins=100)