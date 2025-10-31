
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
        self.tau = tau
        self.kappa_3 = kappa_3
        self.Q = Q
        self.R = R
        self.delta_t = delta_t
        self.rng = np.random.default_rng(seed)
        self.label = int(self.tau * self.kappa_3 > 1)
        self.deterministic = self.kappa_3 * \
            np.sqrt(max(0, self.tau - 1.0 / self.kappa_3) / self.Q)

    def __call__(self, v):
        '''
        returns deterministic dynamic = acceleration (without noise)
        :param v: initial velocity vector
        :rtype v: ndarray
        :return: velocity vector of next time step
        :return type: ndarray
        '''
        v_norm = np.linalg.norm(v)
        deterministic_acceleration = (
            self.tau - self.kappa_3 - self.Q * v_norm**2) * v
        return v + deterministic_acceleration * self.delta_t

    def simulate(self, N, v0=np.zeros(2)):
        v = np.zeros((N, len(v0)))
        v[0] = v0
        for i in range(1, N):
            v[i] = self(v[i-1]) + self.R * \
                self.rng.normal(size=len(v0)) * np.sqrt(self.delta_t)
        return v
