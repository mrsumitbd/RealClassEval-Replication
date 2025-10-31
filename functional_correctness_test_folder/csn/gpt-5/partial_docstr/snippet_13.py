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

        self._rng = np.random.default_rng(seed)

        threshold = 1.0 / self.kappa_3
        self.label = 1 if self.tau > threshold else 0

        mu = (self.tau - threshold) / self.Q
        mu = max(mu, 0.0)
        self.deterministic = self.kappa_3 * np.sqrt(mu)

    def __call__(self, v):
        '''
        returns deterministic dynamic = acceleration (without noise)
        :param v: initial velocity vector
        :rtype v: ndarray
        :return: velocity vector of next time step
        :return type: ndarray
        '''
        v = np.asarray(v, dtype=float)
        mu = (self.tau - 1.0 / self.kappa_3) / self.Q
        a = mu
        b = 1.0 / (self.kappa_3 ** 2)
        v_norm_sq = np.dot(v, v)
        return a * v - b * v_norm_sq * v

    def simulate(self, N, v0=np.zeros(2)):
        v = np.asarray(v0, dtype=float).copy()
        traj = np.empty((N, v.shape[0]), dtype=float)
        dt = self.delta_t
        noise_scale = np.sqrt(2.0 * self.R * dt) if self.R > 0.0 else 0.0

        for i in range(N):
            det = self.__call__(v)
            if noise_scale > 0.0:
                eta = self._rng.normal(0.0, 1.0, size=v.shape)
                v = v + det * dt + noise_scale * eta
            else:
                v = v + det * dt
            traj[i] = v

        return traj
