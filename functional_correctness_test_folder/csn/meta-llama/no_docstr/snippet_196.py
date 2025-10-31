
class Mechanism:

    def __init__(self, mechanism, param=None):
        self.mechanism = mechanism
        self.param = param

    def to_native(self):
        if self.mechanism == 'laplace':
            if self.param is None:
                raise ValueError(
                    "Laplace mechanism requires a sensitivity parameter")
            return f"Laplace({self.param})"
        elif self.mechanism == 'gaussian':
            if self.param is None or len(self.param) != 2:
                raise ValueError(
                    "Gaussian mechanism requires a tuple of (sensitivity, epsilon) parameters")
            return f"Gaussian(sensitivity={self.param[0]}, epsilon={self.param[1]})"
        else:
            raise ValueError(f"Unsupported mechanism: {self.mechanism}")
