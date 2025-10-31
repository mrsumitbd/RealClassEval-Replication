import numpy as np

class Tau_Local_Neighbor:
    """
    Neighbor set LIMA.

    Local concordance relationships between a focal unit and its
    neighbors. A decomposition of local Tau into neighbor and
    non-neighbor components.

    Parameters
    ----------
    x              : array
                     (n, ), first variable.
    y              : array
                     (n, ), second variable.
    w              : W
                     spatial weights object.
    permutations   : int
                     number of random spatial permutations for
                     computationally based inference.

    Attributes
    ----------
    n              : int
                     number of observations.
    tau_local       : array
                     (n, ), local concordance (local version of the
                     classic tau).
    S              : array
                     (n ,n), concordance matrix, s_{i,j}=1 if
                     observation i and j are concordant, s_{i,
                     j}=-1 if observation i and j are discordant,
                     and s_{i,j}=0 otherwise.
    tau_ln         : array
                     (n, ), observed neighbor set LIMA values.
    tau_ln_weights : array
                     (n, ), weights for neighbor set LIMA at each
                     location. GIMA is the weighted average of
                     neighbor set LIMA.
    tau_ln_sim     : array
                     (n, permutations), neighbor set LIMA values for
                     permuted samples (if permutations>0).
    tau_ln_pvalues : array
                     (n, ), one-sided pseudo p-values for observed neighbor
                     set LIMA values under the null that concordance
                     relationship between the focal state and itsn
                     eighbors is not different from what could be
                     expected from randomly distributed rank changes.
    sign           : array
                     (n, ), values indicate concordant or
                     disconcordant: 1 concordant, -1 disconcordant

    Notes
    -----
    The equation for calculating neighbor set LIMA statistic can be
    found in :cite:`Rey2016` Equation (16).

    Examples
    --------
    >>> import libpysal as ps
    >>> import numpy as np
    >>> from giddy.rank import Tau_Local_Neighbor, SpatialTau
    >>> np.random.seed(10)
    >>> f = ps.io.open(ps.examples.get_path("mexico.csv"))
    >>> vnames = ["pcgdp%d"%dec for dec in range(1940, 2010, 10)]
    >>> y = np.transpose(np.array([f.by_col[v] for v in vnames]))
    >>> r = y / y.mean(axis=0)
    >>> regime = np.array(f.by_col['esquivel99'])
    >>> w = ps.weights.block_weights(regime)
    >>> res = Tau_Local_Neighbor(r[:,0], r[:,1], w, permutations=999)
    >>> res.tau_ln
    array([-0.2       ,  1.        ,  1.        ,  1.        ,  0.33333333,
            0.6       ,  0.6       , -0.5       ,  1.        ,  1.        ,
            0.2       ,  0.33333333,  0.33333333,  0.5       ,  1.        ,
            1.        ,  1.        ,  0.        ,  0.6       , -0.33333333,
           -0.33333333, -0.6       ,  1.        ,  0.2       ,  0.        ,
            0.2       ,  1.        ,  0.6       ,  0.33333333,  0.5       ,
            0.5       , -0.2       ])
    >>> res.tau_ln_weights
    array([0.03968254, 0.03968254, 0.03174603, 0.03174603, 0.02380952,
           0.03968254, 0.03968254, 0.03174603, 0.00793651, 0.03968254,
           0.03968254, 0.02380952, 0.02380952, 0.03174603, 0.00793651,
           0.02380952, 0.02380952, 0.03174603, 0.03968254, 0.02380952,
           0.02380952, 0.03968254, 0.03174603, 0.03968254, 0.03174603,
           0.03968254, 0.03174603, 0.03968254, 0.02380952, 0.03174603,
           0.03174603, 0.03968254])
    >>> res.tau_ln_pvalues
    array([0.541, 0.852, 0.668, 0.568, 0.11 , 0.539, 0.609, 0.058, 1.   ,
           0.255, 0.125, 0.087, 0.393, 0.433, 0.908, 0.657, 0.447, 0.128,
           0.531, 0.033, 0.12 , 0.271, 0.868, 0.234, 0.124, 0.387, 0.859,
           0.697, 0.349, 0.664, 0.596, 0.041])
    >>> res.sign
    array([-1,  1,  1,  1,  1,  1,  1, -1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
            1,  1, -1, -1, -1,  1,  1,  1,  1,  1,  1,  1,  1,  1, -1])
    >>> (res.tau_ln * res.tau_ln_weights).sum() #global spatial tau
    np.float64(0.39682539682539675)
    >>> res1 = SpatialTau(r[:,0],r[:,1],w,permutations=999)
    >>> res1.tau_spatial
    np.float64(0.3968253968253968)

    """

    def __init__(self, x, y, w, permutations=0):
        x = np.asarray(x)
        y = np.asarray(y)
        self.n = len(x)
        w.transform = 'b'
        self.tau_ln, self.tau_ln_weights = self._calc(x, y, w)
        concor_sign = np.ones(self.n)
        concor_sign[self.tau_ln < 0] = -1
        self.sign = concor_sign.astype(int)
        if permutations > 0:
            tau_ln_sim = np.zeros((self.n, permutations))
            tau_ln_pvalues = np.zeros(self.n)
            for i in range(self.n):
                obs_i = self.tau_ln[i]
                yr = np.zeros_like(y)
                xr = np.zeros_like(y)
                rids = np.arange(self.n)
                rids = np.delete(rids, i)
                for j in range(permutations):
                    pids = np.random.permutation(rids)
                    xr[i] = x[i]
                    xr[rids] = x[pids]
                    yr[i] = y[i]
                    yr[rids] = y[pids]
                    tau_ln_sim[i, j] = self._calc(xr, yr, w, i)
                larger = (tau_ln_sim[i] >= obs_i).sum()
                smaller = (tau_ln_sim[i] <= obs_i).sum()
                tau_ln_pvalues[i] = (np.min([larger, smaller]) + 1.0) / (1 + permutations)
            self.tau_ln_sim = tau_ln_sim
            self.tau_ln_pvalues = tau_ln_pvalues

    def _calc_r(self, xi, yi, xj, yj, w):
        dx = xi - xj
        dy = yi - yj
        dxdy = dx * dy
        if dxdy != 0:
            if dxdy > 0.0:
                return 1
            else:
                return -1
        else:
            return 0

    def _calc(self, x, y, w, i=None):
        if i is not None:
            iS_local = 0
            for j in w.neighbors[i]:
                iS_local += self._calc_r(x[i], y[i], x[j], y[j], w)
            tau_ln = iS_local * 1.0 / w.cardinalities[i]
            return tau_ln
        else:
            tau_ln = np.zeros(self.n)
            tau_ln_weights = np.zeros(self.n)
            for i in w.id_order:
                iS_local = 0
                for j in w.neighbors[i]:
                    iS_local += self._calc_r(x[i], y[i], x[j], y[j], w)
                tau_ln[i] = iS_local * 1.0 / w.cardinalities[i]
                tau_ln_weights[i] = w.cardinalities[i] * 1.0 / w.s0
            return (tau_ln, tau_ln_weights)