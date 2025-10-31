import numpy as np
from scipy.stats.mstats import rankdata

class Theta:
    """
    Regime mobility measure. :cite:`Rey2004a`

    For sequence of time periods Theta measures the extent to which rank
    changes for a variable measured over n locations are in the same direction
    within mutually exclusive and exhaustive partitions (regimes) of the n locations.

    Theta is defined as the sum of the absolute sum of rank changes within
    the regimes over the sum of all absolute rank changes.

    Parameters
    ----------
    y            : array
                   (n, k) with k>=2, successive columns of y are later moments
                   in time (years, months, etc).
    regime       : array
                   (n, ), values corresponding to which regime each observation
                   belongs to.
    permutations : int
                   number of random spatial permutations to generate for
                   computationally based inference.

    Attributes
    ----------
    ranks        : array
                   ranks of the original y array (by columns).
    regimes      : array
                   the original regimes array.
    total        : array
                   (k-1, ), the total number of rank changes for each of the
                   k periods.
    max_total    : int
                   the theoretical maximum number of rank changes for n
                   observations.
    theta        : array
                   (k-1,), the theta statistic for each of the k-1 intervals.
    permutations : int
                   the number of permutations.
    pvalue_left  : float
                   p-value for test that observed theta is significantly lower
                   than its expectation under complete spatial randomness.
    pvalue_right : float
                   p-value for test that observed theta is significantly
                   greater than its expectation under complete spatial randomness.

    Examples
    --------
    >>> import libpysal as ps
    >>> from giddy.rank import Theta
    >>> import numpy as np
    >>> f=ps.io.open(ps.examples.get_path("mexico.csv"))
    >>> vnames=["pcgdp%d"%dec for dec in range(1940,2010,10)]
    >>> y=np.transpose(np.array([f.by_col[v] for v in vnames]))
    >>> regime=np.array(f.by_col['esquivel99'])
    >>> np.random.seed(10)
    >>> t=Theta(y,regime,999)
    >>> t.theta
    array([[0.41538462, 0.28070175, 0.61363636, 0.62222222, 0.33333333,
            0.47222222]])
    >>> t.pvalue_left
    array([0.307, 0.077, 0.823, 0.552, 0.045, 0.735])
    >>> t.total
    array([130., 114.,  88.,  90.,  90.,  72.])
    >>> t.max_total
    512

    """

    def __init__(self, y, regime, permutations=999):
        ranks = rankdata(y, axis=0)
        self.ranks = ranks
        n, k = y.shape
        ranks_d = ranks[:, list(range(1, k))] - ranks[:, list(range(k - 1))]
        self.ranks_d = ranks_d
        regimes = np.unique(regime)
        self.regimes = regimes
        self.total = sum(abs(ranks_d))
        self.max_total = sum([abs(i - n + i - 1) for i in range(1, n + 1)])
        self._calc(regime)
        self.theta = self._calc(regime)
        self.permutations = permutations
        if permutations:
            np.perm = np.random.permutation
            sim = np.array([self._calc(np.perm(regime)) for i in range(permutations)])
            self.theta.shape = (1, len(self.theta))
            sim = np.concatenate((self.theta, sim))
            self.sim = sim
            den = permutations + 1.0
            self.pvalue_left = (sim <= sim[0]).sum(axis=0) / den
            self.pvalue_right = (sim > sim[0]).sum(axis=0) / den
            self.z = (sim[0] - sim.mean(axis=0)) / sim.std(axis=0)

    def _calc(self, regime):
        within = [abs(sum(self.ranks_d[regime == reg])) for reg in self.regimes]
        return np.array(sum(within) / self.total)