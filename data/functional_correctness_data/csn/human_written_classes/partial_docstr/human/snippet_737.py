import numpy as np
import toyplot

class TreeSampler:
    """
    Class for applying uncorrelated gamma rate transformations to edges
    to create Generative data for testing the Chronos functions.
    """

    def __init__(self, tree, neff=500000.0, gentime=1, gamma=3):
        self.tree = tree
        self.neff = neff
        self.gentime = gentime
        self.gamma = gamma
        self.nnodes = self.tree.nnodes

    def plot_gamma_distributed_rates(self, nsamples=10000, bins=30):
        """
        Draws the stat distribution for verification.
        """
        a = (1 / self.gamma) ** 2
        b = 1
        gamma_rates = np.random.gamma(shape=1 / (a * b ** 2), scale=a * b ** 2, size=nsamples)
        NEVAR = gamma_rates * self.neff
        canvas = toyplot.Canvas(width=600, height=250)
        ax0 = canvas.cartesian(grid=(1, 2, 0), xlabel='gamma distributed Ne variation')
        m0 = ax0.bars(np.histogram(NEVAR, bins=bins))
        GVAR = gamma_rates * self.gentime
        ax1 = canvas.cartesian(grid=(1, 2, 1), xlabel='gamma distributed gentime variation')
        m1 = ax1.bars(np.histogram(GVAR, bins=bins))
        return (canvas, (ax0, ax1), (m0, m1))

    def get_tree(self, N=False, G=False, transform=False, seed=None):
        """
        N (bool):
            Sample gamma distributed variation in Ne values across nodes.
        G (bool):
            Sample gamma distributed variation in G values across nodes.
        transform (int):
            Return edge lengths in requested units by selecting integer value:
            (0) time, (1) coalunits, (2) generations.    
        """
        tree = self.tree.copy()
        if seed:
            np.random.seed(seed)
        a = (1 / self.gamma) ** 2
        b = 1
        if N:
            gamma_rates = np.random.gamma(shape=1 / (a * b ** 2), scale=a * b ** 2, size=self.nnodes)
            nevals = gamma_rates * self.neff
            tree = tree.set_node_data(feature='Ne', data={i: nevals[i] for i in range(tree.nnodes)})
        else:
            tree = tree.set_node_data('Ne', default=self.neff)
        if G:
            gamma_rates = np.random.gamma(shape=1 / (a * b ** 2), scale=a * b ** 2, size=self.nnodes)
            gvals = gamma_rates * self.gentime
            tree = tree.set_node_data(feature='g', data={i: gvals[i] for i in range(tree.nnodes)})
        else:
            tree = tree.set_node_data('g', default=self.gentime)
        if transform == 1:
            tree = tree.set_node_data(feature='dist', data={i: j.dist / (j.Ne * 2 * j.g) for i, j in enumerate(tree)})
        elif transform == 2:
            tree = tree.set_node_data(feature='dist', data={i: j.dist / j.g for i, j in enumerate(tree)})
        return tree