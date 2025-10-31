import numpy as np
from scipy.special import erfc

class Tau:
    """
    Kendall's Tau is based on a comparison of the number of pairs of n
    observations that have concordant ranks between two variables.

    Parameters
    ----------
    x            : array
                   (n, ), first variable.
    y            : array
                   (n, ), second variable.

    Attributes
    ----------
    tau          : float
                   The classic Tau statistic.
    tau_p        : float
                   asymptotic p-value.

    Notes
    -----
    Modification of algorithm suggested by :cite:`Christensen2005`.PySAL/giddy
    implementation uses a list based representation of a binary tree for
    the accumulation of the concordance measures. Ties are handled by this
    implementation (in other words, if there are ties in either x, or y, or
    both, the calculation returns Tau_b, if no ties classic Tau is returned.)

    Examples
    --------
    >>> from scipy.stats import kendalltau
    >>> from giddy.rank import Tau
    >>> x1 = [12, 2, 1, 12, 2]
    >>> x2 = [1, 4, 7, 1, 0]
    >>> kt = Tau(x1,x2)
    >>> print("%.5f" % kt.tau)
    -0.47140
    >>> print("%.5f" % kt.tau_p)
    0.24821
    >>> tau, p = kendalltau(x1,x2)
    >>> print("%.5f" % tau)
    -0.47140
    >>> print("%.5f" % p)
    0.28275

    """

    def __init__(self, x, y):
        res = self._calc(x, y)
        self.tau = res[0]
        self.tau_p = res[1]
        self.concordant = res[2]
        self.discordant = res[3]
        self.extraX = res[4]
        self.extraY = res[5]

    def _calc(self, x, y):
        """
        List based implementation of binary tree algorithm for concordance
        measure after :cite:`Christensen2005`.

        """
        x = np.array(x)
        y = np.array(y)
        n = len(y)
        perm = list(range(n))
        perm.sort(key=lambda a: (x[a], y[a]))
        ExtraY = 0
        ExtraX = 0
        ACount = 0
        BCount = 0
        CCount = 0
        DCount = 0
        ECount = 1
        DCount = 0
        Concordant = 0
        Discordant = 0
        li = [None] * (n - 1)
        ri = [None] * (n - 1)
        ld = np.zeros(n)
        nequal = np.zeros(n)
        for i in range(1, n):
            NumBefore = 0
            NumEqual = 1
            root = 0
            x0 = x[perm[i - 1]]
            y0 = y[perm[i - 1]]
            x1 = x[perm[i]]
            y1 = y[perm[i]]
            if x0 != x1:
                DCount = 0
                ECount = 1
            elif y0 == y1:
                ECount += 1
            else:
                DCount += ECount
                ECount = 1
            root = 0
            inserting = True
            while inserting:
                current = y[perm[i]]
                if current > y[perm[root]]:
                    NumBefore += 1 + ld[root] + nequal[root]
                    if ri[root] is None:
                        ri[root] = i
                        inserting = False
                    else:
                        root = ri[root]
                elif current < y[perm[root]]:
                    ld[root] += 1
                    if li[root] is None:
                        li[root] = i
                        inserting = False
                    else:
                        root = li[root]
                elif current == y[perm[root]]:
                    NumBefore += ld[root]
                    NumEqual += nequal[root] + 1
                    nequal[root] += 1
                    inserting = False
            ACount = NumBefore - DCount
            BCount = NumEqual - ECount
            CCount = i - (ACount + BCount + DCount + ECount - 1)
            ExtraY += DCount
            ExtraX += BCount
            Concordant += ACount
            Discordant += CCount
        cd = Concordant + Discordant
        num = Concordant - Discordant
        tau = num / np.sqrt((cd + ExtraX) * (cd + ExtraY))
        v = (4.0 * n + 10) / (9.0 * n * (n - 1))
        z = tau / np.sqrt(v)
        pval = erfc(np.abs(z) / 1.4142136)
        return (tau, pval, Concordant, Discordant, ExtraX, ExtraY)