import numpy as np

class SpatialTau:
    """
    Spatial version of Kendall's rank correlation statistic.

    Kendall's Tau is based on a comparison of the number of pairs of n
    observations that have concordant ranks between two variables. The spatial
    Tau decomposes these pairs into those that are spatial neighbors and those
    that are not, and examines whether the rank correlation is different
    between the two sets relative to what would be expected under spatial randomness.

    Parameters
    ----------
    x             : array
                    (n, ), first variable.
    y             : array
                    (n, ), second variable.
    w             : W
                    spatial weights object.
    permutations  : int
                    number of random spatial permutations for computationally
                    based inference.

    Attributes
    ----------
    tau                : float
                         The classic Tau statistic.
    tau_spatial        : float
                         Value of Tau for pairs that are spatial neighbors.
    taus               : array
                         (permtuations, 1), values of simulated tau_spatial values
                         under random spatial permutations in both periods. (Same
                         permutation used for start and ending period).
    pairs_spatial      : int
                         Number of spatial pairs.
    concordant         : float
                         Number of concordant pairs.
    concordant_spatial : float
                         Number of concordant pairs that are spatial neighbors.
    extraX             : float
                         Number of extra X pairs.
    extraY             : float
                         Number of extra Y pairs.
    discordant         : float
                         Number of discordant pairs.
    discordant_spatial : float
                         Number of discordant pairs that are spatial neighbors.
    taus               : float
                         spatial tau values for permuted samples (if permutations>0).
    tau_spatial_psim   : float
                         one-sided pseudo p-value for observed tau_spatial
                         under the null of spatial randomness of rank exchanges
                         (if permutations>0).

    Notes
    -----
    Algorithm has two stages. The first calculates classic Tau using a list
    based implementation of the algorithm from :cite:`Christensen2005`. Second
    stage calculates concordance measures for neighboring pairs of locations
    using a modification of the algorithm from :cite:`Press2007`. See
    :cite:`Rey2014` for details.

    Examples
    --------
    >>> import libpysal as ps
    >>> import numpy as np
    >>> from giddy.rank import SpatialTau
    >>> f=ps.io.open(ps.examples.get_path("mexico.csv"))
    >>> vnames=["pcgdp%d"%dec for dec in range(1940,2010,10)]
    >>> y=np.transpose(np.array([f.by_col[v] for v in vnames]))
    >>> regime=np.array(f.by_col['esquivel99'])
    >>> w=ps.weights.block_weights(regime)
    >>> np.random.seed(12345)
    >>> res=[SpatialTau(y[:,i],y[:,i+1],w,99) for i in range(6)]
    >>> for r in res:
    ...     ev = r.taus.mean()
    ...     "%8.3f %8.3f %8.3f"%(r.tau_spatial, ev, r.tau_spatial_psim)
    ...
    '   0.397    0.659    0.010'
    '   0.492    0.706    0.010'
    '   0.651    0.772    0.020'
    '   0.714    0.752    0.210'
    '   0.683    0.705    0.270'
    '   0.810    0.819    0.280'
    """

    def __init__(self, x, y, w, permutations=0):
        w.transform = 'b'
        self.n = len(x)
        res = Tau(x, y)
        self.tau = res.tau
        self.tau_p = res.tau_p
        self.concordant = res.concordant
        self.discordant = res.discordant
        self.extraX = res.extraX
        self.extraY = res.extraY
        res = self._calc(x, y, w)
        self.tau_spatial = res[0]
        self.pairs_spatial = int(w.s0 / 2.0)
        self.concordant_spatial = res[1]
        self.discordant_spatial = res[2]
        if permutations > 0:
            taus = np.zeros(permutations)
            ids = np.arange(self.n)
            for r in range(permutations):
                rids = np.random.permutation(ids)
                taus[r] = self._calc(x[rids], y[rids], w)[0]
            self.taus = taus
            self.tau_spatial_psim = pseudop(taus, self.tau_spatial, permutations)

    def _calc(self, x, y, w):
        n1 = n2 = iS = gc = 0
        ijs = {}
        for i in w.id_order:
            xi = x[i]
            yi = y[i]
            for j in w.neighbors[i]:
                if i < j:
                    ijs[i, j] = (i, j)
                    xj = x[j]
                    yj = y[j]
                    dx = xi - xj
                    dy = yi - yj
                    dxdy = dx * dy
                    if dxdy != 0:
                        n1 += 1
                        n2 += 1
                        if dxdy > 0.0:
                            gc += 1
                            iS += 1
                        else:
                            iS -= 1
                    else:
                        if dx != 0.0:
                            n1 += 1
                        if dy != 0.0:
                            n2 += 1
        tau_g = iS / (np.sqrt(n1) * np.sqrt(n2))
        gd = gc - iS
        return [tau_g, gc, gd]