import numpy as np


class velocity:
    '''
    Simulates the velocity of a dissipative soliton (kind of self organized particle) [6]_.
    The equilibrium velocity without noise R=0 for
    $    au>1.0/\kappa_3$ is $\kappa_3 \sqrt{(tau - 1.0/\kappa_3)/Q}.
    Before the drift-bifurcation $    au \le 1.0/\kappa_3$ the velocity is zero.
    References
    ----------
    .. [6] Andreas Kempa-Liehr (2013, p. 159-170)
        Dynamics of Dissipative Soliton
        Dissipative Solitons in Reaction Diffusion Systems.
        Springer: Berlin
    >>> ds = velocity(tau=3.5) # Dissipative soliton with equilibrium velocity 1.5e-3
    >>> print(ds.label) # Discriminating before or beyond Drift-Bifurcation
    1
    # Equilibrium velocity
    >>> print(ds.deterministic)
    0.0015191090506254991
    # Simulated velocity as a time series with 20000 time steps being disturbed by Gaussian white noise
    >>> v = ds.simulate(20000)
    '''

    def __init__(self, tau=3.8, kappa_3=0.3, Q=1950.0, R=0.0003, delta_t=0.05, seed=None):
        self.tau = float(tau)
        self.kappa_3 = float(kappa_3)
        self.Q = float(Q)
        self.R = float(R)
        self.delta_t = float(delta_t)
        self.rng = np.random.default_rng(seed)

        self._inv_k3 = 1.0 / self.kappa_3
        self.label = 1 if self.tau > self._inv_k3 else 0

        # Parameters for deterministic dynamics: dv/dt = (a - b |v|^2) v
        self.a = (self.kappa_3 ** 2) * (self.tau - self._inv_k3)
        self.b = self.Q / self.kappa_3

        # Equilibrium speed (deterministic, without noise)
        if self.label == 1:
            self.deterministic = self.kappa_3 * \
                np.sqrt((self.tau - self._inv_k3) / self.Q)
        else:
            self.deterministic = 0.0

    def __call__(self, v):
        '''
        returns deterministic dynamic = acceleration (without noise)
        :param v: initial velocity vector
        :rtype v: ndarray
        :return: velocity vector of next time step
        :return type: ndarray
        '''
        v = np.asarray(v, dtype=float)
        if v.ndim == 1:
            norm2 = np.dot(v, v)
            dv = (self.a - self.b * norm2) * v
        else:
            norm2 = np.sum(v * v, axis=-1, keepdims=True)
            dv = (self.a - self.b * norm2) * v
        return v + self.delta_t * dv

    def simulate(self, N, v0=np.zeros(2)):
        N = int(N)
        v = np.array(v0, dtype=float).reshape(2)
        out = np.empty((N, 2), dtype=float)
        sigma = np.sqrt(2.0 * self.R * self.delta_t)

        for i in range(N):
            # Deterministic update
            norm2 = np.dot(v, v)
            dv = (self.a - self.b * norm2) * v
            # Stochastic term (Gaussian white noise)
            eta = sigma * self.rng.normal(size=2)
            v = v + self.delta_t * dv + eta
            out[i] = v

        return out
