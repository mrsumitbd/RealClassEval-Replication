from autograd import numpy as anp
import numpy as np

class SplineFitterMixin:

    @staticmethod
    def relu(x: np.ndarray):
        return anp.maximum(0, x)

    def basis(self, x: np.ndarray, knot: float, min_knot: float, max_knot: float):
        lambda_ = (max_knot - knot) / (max_knot - min_knot)
        return self.relu(x - knot) ** 3 - (lambda_ * self.relu(x - min_knot) ** 3 + (1 - lambda_) * self.relu(x - max_knot) ** 3)