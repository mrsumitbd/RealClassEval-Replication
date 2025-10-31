import numpy as np

class OnlineSmootherMixin:
    """Mix-in for on-line smoothing algorithms.
    """

    def fetch(self, smc):
        if smc.t == 0:
            self.Phi = smc.fk.add_func(0, None, smc.X)
        else:
            self.update(smc)
        out = np.average(self.Phi, axis=0, weights=smc.W)
        self.save_for_later(smc)
        return out

    def update(self, smc):
        """The part that varies from one (on-line smoothing) algorithm to the
        next goes here.
        """
        raise NotImplementedError

    def save_for_later(self, smc):
        """Save certain quantities that are required in the next iteration."""
        pass