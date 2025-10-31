
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
        self.seed = seed
        self._threshold = 1.0 / self.kappa_3
        self.label = int(self.tau > self._threshold)
        if self.label:
            self.deterministic = self.kappa_3 * \
                np.sqrt((self.tau - self._threshold) / self.Q)
        else:
            self.deterministic = 0.0
        if seed is not None:
            self._rng = np.random.default_rng(seed)
        else:
            self._rng = np.random.default_rng()

    def __call__(self, v):
        v = np.asarray(v)
        v_norm = np.linalg.norm(v)
        if self.label:
            v_eq = self.deterministic
            # deterministic drift: kappa_3 * (tau * v - v * v_norm^2 / v_eq^2)
            if v_eq == 0:
                drift = -self.kappa_3 * v
            else:
                drift = self.kappa_3 * \
                    (self.tau * v - v * (v_norm**2) / (v_eq**2))
        else:
            drift = -self.kappa_3 * v
        return drift

    def simulate(self, N, v0=np.zeros(2)):
        v = np.zeros((N, 2))
        v[0] = v0
        sqrt_2Rdt = np.sqrt(2 * self.R * self.delta_t)
        for i in range(1, N):
            drift = self.__call__(v[i-1])
            noise = sqrt_2Rdt * self._rng.normal(size=2)
            v[i] = v[i-1] + drift * self.delta_t + noise
        return v
