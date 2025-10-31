class ArrayMCMC:
    """Base class for a (single) MCMC step applied to an array.

    To implement a particular MCMC scheme, subclass ArrayMCMC and define method
    ``step(self, x, target=None)``, which applies one step to all the particles
    in object ``xx``, for a given target distribution ``target``).
    Additionally, you may also define method ``calibrate(self, W, x)`` which will
    be called before resampling in order to tune the MCMC step on the weighted
    sample (W, x).

    """

    def __init__(self):
        pass

    def calibrate(self, W, x):
        """
        Parameters
        ----------
        W:  (N,) numpy array
            weights
        x:  ThetaParticles object
            particles
        """
        pass

    def step(self, x, target=None):
        """
        Parameters
        ----------
        x:   particles object
            current particle system (will be modified in-place)
        target: callable
            compute fields such as x.lpost (log target density)

        Returns
        -------
        mean acceptance probability

        """
        raise NotImplementedError