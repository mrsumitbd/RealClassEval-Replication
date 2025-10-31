import numpy as np

class Weights:
    """ A class to store N log-weights, and automatically compute normalised
    weights and their ESS.

    Parameters
    ----------
    lw : (N,) array or None
        log-weights (if None, object represents a set of equal weights)

    Attributes
    ----------
    lw : (N), array
        log-weights (un-normalised)
    W : (N,) array
        normalised weights
    ESS : scalar
        the ESS (effective sample size) of the weights

    Warning
    -------
    Objects of this class should be considered as immutable; in particular,
    method add returns a *new* object. Trying to modifying directly the
    log-weights may introduce bugs.

    """

    def __init__(self, lw=None):
        self.lw = lw
        if lw is not None:
            self.lw[np.isnan(self.lw)] = -np.inf
            m = self.lw.max()
            w = np.exp(self.lw - m)
            s = w.sum()
            self.log_mean = m + np.log(s / self.N)
            self.W = w / s
            self.ESS = 1.0 / np.sum(self.W ** 2)

    @property
    def N(self):
        return 0 if self.lw is None else self.lw.shape[0]

    def add(self, delta):
        """Increment weights: lw <-lw + delta.

        Parameters
        ----------
        delta : (N,) array
            incremental log-weights

        """
        if self.lw is None:
            return self.__class__(lw=delta)
        else:
            return self.__class__(lw=self.lw + delta)