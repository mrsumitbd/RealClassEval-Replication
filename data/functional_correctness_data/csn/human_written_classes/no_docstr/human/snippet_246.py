import arviz as az
import numpy as np

class Atleast_Nd:
    params = ('az.utils', 'numpy')
    param_names = ('source',)

    def setup(self, source):
        self.data = np.random.randn(100000)
        self.x = np.random.randn(100000).tolist()
        if source == 'az.utils':
            self.atleast_2d = az.utils.two_de
            self.atleast_1d = az.utils.one_de
        else:
            self.atleast_2d = np.atleast_2d
            self.atleast_1d = np.atleast_1d

    def time_atleast_2d_array(self, source):
        self.atleast_2d(self.data)

    def time_atleast_1d(self, source):
        self.atleast_1d(self.x)