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
        '''
        :param tau: Bifurcation parameter determining the intrinsic velocity of the dissipative soliton,
                    which is zero for tau<=1.0/kappa_3 and np.sqrt(kappa_3**3/Q * (tau - 1.0/kappa_3)) otherwise
        :type tau: float
        :param kappa_3: Inverse bifurcation point.
        :type kappa_3:
        :param Q: Shape parameter of dissipative soliton
        :type Q: float
        :param R: Noise amplitude
        :type R: float
        :param delta_t: temporal discretization
        :type delta_t: float
        '''
        self.tau = float(tau)
        self.kappa_3 = float(kappa_3)
        self.Q = float(Q)
        self.R = float(R)
        self.delta_t = float(delta_t)
        self.seed = seed
        self.rng = np.random.default_rng(seed)

        inv_bif = 1.0 / self.kappa_3
        self._a = self.kappa_3**3 * (self.tau - inv_bif)

        if self._a > 0.0:
            self.label = 1
            self.deterministic = float(np.sqrt(self._a / self.Q))
        else:
            self.label = 0
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
        r2 = np.dot(v, v)
        drift = self._a * v - self.Q * r2 * v
        return v + self.delta_t * drift

    def simulate(self, N, v0=np.zeros(2)):
        '''
        :param N: number of time steps
        :type N: int
        :param v0: initial velocity vector
        :type v0: ndarray
        :return: time series of velocity vectors with shape (N, v0.shape[0])
        :rtype: ndarray
        '''
        v0 = np.asarray(v0, dtype=float)
        if v0.ndim == 0:
            v0 = v0[None]
        d = v0.shape[0]
        traj = np.empty((N, d), dtype=float)
        traj[0] = v0

        sqrt_dt = np.sqrt(self.delta_t)
        for t in range(1, N):
            v_prev = traj[t - 1]
            v_det = self.__call__(v_prev)
            if self.R != 0.0:
                noise = self.R * sqrt_dt * self.rng.standard_normal(d)
                traj[t] = v_det + noise
            else:
                traj[t] = v_det
        return traj
