import numpy as np
from libpysal import weights

class Tau_Regional:
    """
    Inter and intraregional decomposition of the classic Tau.

    Parameters
    ----------
    x               : array
                      (n, ), first variable.
    y               : array
                      (n, ), second variable.
    regimes         : array
                      (n, ), ids of which regime an observation belongs to.
    permutations    : int
                      number of random spatial permutations for
                      computationally based inference.

    Attributes
    ----------
    n               : int
                      number of observations.
    S               : array
                      (n ,n), concordance matrix, s_{i,j}=1 if
                      observation i and j are concordant, s_{i,
                      j}=-1 if observation i and j are discordant,
                      and s_{i,j}=0 otherwise.
    tau_reg         : array
                      (k, k), observed concordance matrix with
                      diagonal elements measuring concordance
                      between units within a regime and the
                      off-diagonal elements denoting concordance
                      between observations from a specific
                      pair of different regimes.
    tau_reg_sim     : array
                      (permutations, k, k), concordance matrices for
                      permuted samples (if permutations>0).
    tau_reg_pvalues : array
                      (k, k), one-sided pseudo p-values for observed
                      concordance matrix under the null that income
                      mobility were random in its spatial distribution.

    Notes
    -----
    The equation for calculating inter and intraregional Tau
    statistic can be found in :cite:`Rey2016` Equation (27).

    Examples
    --------
    >>> import libpysal as ps
    >>> import numpy as np
    >>> from giddy.rank import Tau_Regional
    >>> np.random.seed(10)
    >>> f = ps.io.open(ps.examples.get_path("mexico.csv"))
    >>> vnames = ["pcgdp%d"%dec for dec in range(1940, 2010, 10)]
    >>> y = np.transpose(np.array([f.by_col[v] for v in vnames]))
    >>> r = y / y.mean(axis=0)
    >>> regime = np.array(f.by_col['esquivel99'])
    >>> res = Tau_Regional(y[:,0],y[:,-1],regime,permutations=999)
    >>> res.tau_reg
    array([[1.        , 0.25      , 0.5       , 0.6       , 0.83333333,
            0.6       , 1.        ],
           [0.25      , 0.33333333, 0.5       , 0.3       , 0.91666667,
            0.4       , 0.75      ],
           [0.5       , 0.5       , 0.6       , 0.4       , 0.38888889,
            0.53333333, 0.83333333],
           [0.6       , 0.3       , 0.4       , 0.2       , 0.4       ,
            0.28      , 0.8       ],
           [0.83333333, 0.91666667, 0.38888889, 0.4       , 0.6       ,
            0.73333333, 1.        ],
           [0.6       , 0.4       , 0.53333333, 0.28      , 0.73333333,
            0.8       , 0.8       ],
           [1.        , 0.75      , 0.83333333, 0.8       , 1.        ,
            0.8       , 0.33333333]])
    >>> res.tau_reg_pvalues
    array([[0.782, 0.227, 0.464, 0.638, 0.294, 0.627, 0.201],
           [0.227, 0.352, 0.391, 0.14 , 0.048, 0.252, 0.327],
           [0.464, 0.391, 0.587, 0.198, 0.107, 0.423, 0.124],
           [0.638, 0.14 , 0.198, 0.141, 0.184, 0.089, 0.217],
           [0.294, 0.048, 0.107, 0.184, 0.583, 0.25 , 0.005],
           [0.627, 0.252, 0.423, 0.089, 0.25 , 0.38 , 0.227],
           [0.201, 0.327, 0.124, 0.217, 0.005, 0.227, 0.322]])

    """

    def __init__(self, x, y, regime, permutations=0):
        x = np.asarray(x)
        y = np.asarray(y)
        res = Tau_Local(x, y)
        self.n = res.n
        self.S = res.S
        reg = np.array(regime).flatten()
        ur = np.unique(reg).tolist()
        k = len(ur)
        P = np.zeros((k, self.n))
        for i, r in enumerate(reg):
            P[ur.index(r), i] = 1
        w = weights.block_weights(regime)
        w.transform = 'b'
        W = w.full()[0]
        WH = np.ones((self.n, self.n)) - np.eye(self.n) - W
        self.tau_reg = self._calc(W, WH, P, self.S)
        if permutations > 0:
            tau_reg_sim = np.zeros((permutations, k, k))
            larger = np.zeros((k, k))
            smaller = np.zeros((k, k))
            rids = np.arange(len(x))
            for i in range(permutations):
                np.random.shuffle(rids)
                res = Tau_Local(x[rids], y[rids])
                tau_reg_sim[i] = self._calc(W, WH, P, res.S)
                larger += np.greater_equal(tau_reg_sim[i], self.tau_reg)
                smaller += np.less_equal(tau_reg_sim[i], self.tau_reg)
            m = np.less(smaller, larger)
            pvalues = (1 + m * smaller + (1 - m) * larger) / (1.0 + permutations)
            self.tau_reg_sim = tau_reg_sim
            self.tau_reg_pvalues = pvalues

    def _calc(self, W, WH, P, S):
        nomi = np.dot(P, np.dot(S, P.T))
        denomi = np.dot(P, np.dot(W, P.T)) + np.dot(P, np.dot(WH, P.T))
        T = nomi / denomi
        return T