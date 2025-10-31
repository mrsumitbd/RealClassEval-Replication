class MCMCSequence:
    """Base class for a (fixed length or adaptive) sequence of MCMC steps."""

    def __init__(self, mcmc=None, len_chain=10):
        self.mcmc = ArrayRandomWalk() if mcmc is None else mcmc
        self.nsteps = len_chain - 1

    def calibrate(self, W, x):
        self.mcmc.calibrate(W, x)

    def __call__(self, x, target):
        raise NotImplementedError