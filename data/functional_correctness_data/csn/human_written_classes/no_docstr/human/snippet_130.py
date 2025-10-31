from autograd import numpy as np

class SplineFitter:
    _scipy_fit_method = 'SLSQP'
    _scipy_fit_options = {'ftol': 1e-12}

    @staticmethod
    def relu(x):
        return np.maximum(0, x)

    def basis(self, x, knot, min_knot, max_knot):
        lambda_ = (max_knot - knot) / (max_knot - min_knot)
        return self.relu(x - knot) ** 3 - (lambda_ * self.relu(x - min_knot) ** 3 + (1 - lambda_) * self.relu(x - max_knot) ** 3)