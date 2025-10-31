
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
        self.tau = tau
        self.kappa_3 = kappa_3
        self.Q = Q
        self.R = R
        self.delta_t = delta_t
        self.seed = seed

        self._bifurcation = 1.0 / self.kappa_3
        if self.tau > self._bifurcation:
            self.label = 1
            self._v_eq = self.kappa_3 * \
                np.sqrt((self.tau - self._bifurcation) / self.Q)
        else:
            self.label = 0
            self._v_eq = 0.0

        self.deterministic = self._v_eq

        if self.seed is not None:
            self._rng = np.random.default_rng(self.seed)
        else:
            self._rng = np.random.default_rng()

    def __call__(self, v):
        '''
        returns deterministic dynamic = acceleration (without noise)
        :param v: initial velocity vector
        :rtype v: ndarray
        :return: velocity vector of next time step
        :return type: ndarray
        '''
        v = np.asarray(v)
        v_norm = np.linalg.norm(v)
        if self._v_eq == 0.0:
            v_next = v - self.kappa_3 * v * self.delta_t
        else:
            if v_norm == 0:
                direction = np.zeros_like(v)
            else:
                direction = v / v_norm
            v_next = v + self.kappa_3 * \
                (self._v_eq * direction - v) * self.delta_t
        return v_next

    def simulate(self, N, v0=np.zeros(2)):
        '''
        :param N: number of time steps
        :type N: int
        :param v0: initial velocity vector
        :type v0: ndarray
        :return: time series of velocity vectors with shape (N, v0.shape[0])
        :rtype: ndarray
        '''
        v0 = np.asarray(v0)
        shape = (N, v0.shape[0])
        v_series = np.zeros(shape)
        v = v0.copy()
        for i in range(N):
            # Deterministic update
            v_det = self.__call__(v)
            # Additive Gaussian noise
            noise = self.R * np.sqrt(self.delta_t) * \
                self._rng.standard_normal(v.shape)
            v = v_det + noise
            v_series[i] = v
        return v_series
