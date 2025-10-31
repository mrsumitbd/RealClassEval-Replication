
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
        self.rng = np.random.RandomState(seed)

        self.label = 1 if tau > 1.0 / kappa_3 else 0
        if self.label == 1:
            self.deterministic = kappa_3 * np.sqrt((tau - 1.0 / kappa_3) / Q)
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
        v_norm = np.linalg.norm(v)
        if v_norm == 0:
            if self.tau > 1.0 / self.kappa_3:
                dv_dt = np.array([self.deterministic, 0.0])
            else:
                dv_dt = np.zeros(2)
        else:
            dv_dt = (self.tau - 1.0 / self.kappa_3 -
                     self.Q * v_norm**2 / self.kappa_3**2) * v
        return dv_dt

    def simulate(self, N, v0=np.zeros(2)):
        v = np.zeros((N, 2))
        v[0] = v0
        sqrt_delta_t = np.sqrt(self.delta_t)

        for i in range(1, N):
            deterministic_part = self.__call__(v[i-1]) * self.delta_t
            noise = self.rng.normal(0, self.R * sqrt_delta_t, 2)
            v[i] = v[i-1] + deterministic_part + noise

        return v
