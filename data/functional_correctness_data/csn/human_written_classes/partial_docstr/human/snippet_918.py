from scipy import stats
import numpy as np

class Homogeneity_Results:
    """
    Wrapper class to present homogeneity results.

    Parameters
    ----------
    transition_matrices : list
                          of transition matrices for regimes, all matrices must
                          have same size (r, c). r is the number of rows in
                          the transition matrix and c is the number of columns
                          in the transition matrix.
    regime_names        : sequence
                          Labels for the regimes.
    class_names         : sequence
                          Labels for the classes/states of the Markov chain.
    title               : string
                          Title of the table.

    Attributes
    -----------

    Notes
    -----
    Degrees of freedom adjustment follow the approach in :cite:`Bickenbach2003`.

    Examples
    --------
    See Spatial_Markov above.

    """

    def __init__(self, transition_matrices, regime_names=[], class_names=[], title='Markov Homogeneity Test'):
        self._homogeneity(transition_matrices)
        self.regime_names = regime_names
        self.class_names = class_names
        self.title = title

    def _homogeneity(self, transition_matrices):
        M = np.array(transition_matrices)
        m, r, k = M.shape
        self.k = k
        B = np.zeros((r, m))
        T = M.sum(axis=0)
        self.t_total = T.sum()
        n_i = T.sum(axis=1)
        A_i = (T > 0).sum(axis=1)
        A_im = np.zeros((r, m))
        p_ij = np.dot(np.diag(1.0 / (n_i + (n_i == 0) * 1.0)), T)
        den = p_ij + 1.0 * (p_ij == 0)
        b_i = np.zeros_like(A_i)
        p_ijm = np.zeros_like(M)
        m, n_rows, n_cols = M.shape
        m = 0
        Q = 0.0
        LR = 0.0
        lr_table = np.zeros_like(M)
        q_table = np.zeros_like(M)
        for nijm in M:
            nim = nijm.sum(axis=1)
            B[:, m] = 1.0 * (nim > 0)
            b_i = b_i + 1.0 * (nim > 0)
            p_ijm[m] = np.dot(np.diag(1.0 / (nim + (nim == 0) * 1.0)), nijm)
            num = (p_ijm[m] - p_ij) ** 2
            ratio = num / den
            qijm = np.dot(np.diag(nim), ratio)
            q_table[m] = qijm
            Q = Q + qijm.sum()
            mask = (nijm > 0) * (p_ij > 0)
            A_im[:, m] = (nijm > 0).sum(axis=1)
            unmask = 1.0 * (mask == 0)
            ratio = (mask * p_ijm[m] + unmask) / (mask * p_ij + unmask)
            lr = nijm * np.log(ratio)
            LR = LR + lr.sum()
            lr_table[m] = 2 * lr
            m += 1
        self.dof = int(((b_i - 1) * (A_i - 1)).sum())
        self.Q = Q
        self.Q_p_value = 1 - stats.chi2.cdf(self.Q, self.dof)
        self.LR = LR * 2.0
        self.LR_p_value = 1 - stats.chi2.cdf(self.LR, self.dof)
        self.A = A_i
        self.A_im = A_im
        self.B = B
        self.b_i = b_i
        self.LR_table = lr_table
        self.Q_table = q_table
        self.m = m
        self.p_h0 = p_ij
        self.p_h1 = p_ijm

    def summary(self, file_name=None, title='Markov Homogeneity Test'):
        regime_names = ['%d' % i for i in range(self.m)]
        if self.regime_names:
            regime_names = self.regime_names
        cols = ['P(%s)' % str(regime) for regime in regime_names]
        if not self.class_names:
            self.class_names = list(range(self.k))
        max_col = max([len(col) for col in cols])
        col_width = max([5, max_col])
        n_tabs = self.k
        width = n_tabs * 4 + (self.k + 1) * col_width
        lead = '-' * width
        head = title.center(width)
        contents = [lead, head, lead]
        L = 'Number of regimes: %d' % int(self.m)
        k = 'Number of classes: %d' % int(self.k)
        r = 'Regime names: '
        r += ', '.join(regime_names)
        t = 'Number of transitions: %d' % int(self.t_total)
        contents.append(k)
        contents.append(t)
        contents.append(L)
        contents.append(r)
        contents.append(lead)
        h = '%7s %20s %20s' % ('Test', 'LR', 'Chi-2')
        contents.append(h)
        stat = '%7s %20.3f %20.3f' % ('Stat.', self.LR, self.Q)
        contents.append(stat)
        stat = '%7s %20d %20d' % ('DOF', self.dof, self.dof)
        contents.append(stat)
        stat = '%7s %20.3f %20.3f' % ('p-value', self.LR_p_value, self.Q_p_value)
        contents.append(stat)
        print('\n'.join(contents))
        print(lead)
        cols = ['P(%s)' % str(regime) for regime in self.regime_names]
        if not self.class_names:
            self.class_names = list(range(self.k))
        cols.extend(['%s' % str(cname) for cname in self.class_names])
        max_col = max([len(col) for col in cols])
        col_width = max([5, max_col])
        p0 = []
        line0 = ['{s: <{w}}'.format(s='P(H0)', w=col_width)]
        line0.extend(['{s: >{w}}'.format(s=cname, w=col_width) for cname in self.class_names])
        print('    '.join(line0))
        p0.append('&'.join(line0))
        for i, row in enumerate(self.p_h0):
            line = ['%*s' % (col_width, str(self.class_names[i]))]
            line.extend(['%*.3f' % (col_width, v) for v in row])
            print('    '.join(line))
            p0.append('&'.join(line))
        pmats = [p0]
        print(lead)
        for r, p1 in enumerate(self.p_h1):
            p0 = []
            line0 = ['{s: <{w}}'.format(s='P(%s)' % regime_names[r], w=col_width)]
            line0.extend(['{s: >{w}}'.format(s=cname, w=col_width) for cname in self.class_names])
            print('    '.join(line0))
            p0.append('&'.join(line0))
            for i, row in enumerate(p1):
                line = ['%*s' % (col_width, str(self.class_names[i]))]
                line.extend(['%*.3f' % (col_width, v) for v in row])
                print('    '.join(line))
                p0.append('&'.join(line))
            pmats.append(p0)
            print(lead)
        if file_name:
            k = self.k
            ks = str(k + 1)
            with open(file_name + '.tex', 'w') as f:
                c = []
                fmt = 'r' * (k + 1)
                s = '\\begin{tabular}{|%s|}\\hline\n' % fmt
                s += '\\multicolumn{%s}{|c|}{%s}' % (ks, title)
                c.append(s)
                s = 'Number of classes: %d' % int(self.k)
                c.append('\\hline\\multicolumn{%s}{|l|}{%s}' % (ks, s))
                s = 'Number of transitions: %d' % int(self.t_total)
                c.append('\\multicolumn{%s}{|l|}{%s}' % (ks, s))
                s = 'Number of regimes: %d' % int(self.m)
                c.append('\\multicolumn{%s}{|l|}{%s}' % (ks, s))
                s = 'Regime names: '
                s += ', '.join(regime_names)
                c.append('\\multicolumn{%s}{|l|}{%s}' % (ks, s))
                s = '\\hline\\multicolumn{2}{|l}{%s}' % 'Test'
                s += '&\\multicolumn{2}{r}{LR}&\\multicolumn{2}{r|}{Q}'
                c.append(s)
                s = 'Stat.'
                s = '\\multicolumn{2}{|l}{%s}' % s
                s += '&\\multicolumn{2}{r}{%.3f}' % self.LR
                s += '&\\multicolumn{2}{r|}{%.3f}' % self.Q
                c.append(s)
                s = '\\multicolumn{2}{|l}{%s}' % 'DOF'
                s += '&\\multicolumn{2}{r}{%d}' % int(self.dof)
                s += '&\\multicolumn{2}{r|}{%d}' % int(self.dof)
                c.append(s)
                s = '\\multicolumn{2}{|l}{%s}' % 'p-value'
                s += '&\\multicolumn{2}{r}{%.3f}' % self.LR_p_value
                s += '&\\multicolumn{2}{r|}{%.3f}' % self.Q_p_value
                c.append(s)
                s1 = '\\\\\n'.join(c)
                s1 += '\\\\\n'
                c = []
                for mat in pmats:
                    c.append('\\hline\n')
                    for row in mat:
                        c.append(row + '\\\\\n')
                c.append('\\hline\n')
                c.append('\\end{tabular}')
                s2 = ''.join(c)
                f.write(s1 + s2)