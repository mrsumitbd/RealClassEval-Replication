class PartialParticleHistory:
    """Partial history.

    History that records the particle system only at certain times.
    See `smoothing` module doc for more details.
    """

    def __init__(self, func):
        self.is_save_time = func
        self.X, self.wgts = ({}, {})

    def save(self, smc):
        t = smc.t
        if self.is_save_time(t):
            self.X[t] = smc.X
            self.wgts[t] = smc.wgts