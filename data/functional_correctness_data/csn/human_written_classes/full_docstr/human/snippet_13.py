import numpy as np

class velocity:
    """
    Simulates the velocity of a dissipative soliton (kind of self organized particle) [6]_.
    The equilibrium velocity without noise R=0 for
    $	au>1.0/\\kappa_3$ is $\\kappa_3 \\sqrt{(tau - 1.0/\\kappa_3)/Q}.
    Before the drift-bifurcation $	au \\le 1.0/\\kappa_3$ the velocity is zero.

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
    """

    def __init__(self, tau=3.8, kappa_3=0.3, Q=1950.0, R=0.0003, delta_t=0.05, seed=None):
        """
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
        """
        self.delta_t = delta_t
        self.kappa_3 = kappa_3
        self.Q = Q
        self.tau = tau
        self.a = self.delta_t * kappa_3 ** 2 * (tau - 1.0 / kappa_3)
        self.b = self.delta_t * Q / kappa_3
        self.label = int(tau > 1.0 / kappa_3)
        self.c = np.sqrt(self.delta_t) * R
        self.delta_t = self.delta_t
        if seed is not None:
            np.random.seed(seed)
        if tau <= 1.0 / kappa_3:
            self.deterministic = 0.0
        else:
            self.deterministic = kappa_3 ** 1.5 * np.sqrt((tau - 1.0 / kappa_3) / Q)

    def __call__(self, v):
        """
        returns deterministic dynamic = acceleration (without noise)

        :param v: initial velocity vector
        :rtype v: ndarray
        :return: velocity vector of next time step
        :return type: ndarray
        """
        return v * (1.0 + self.a - self.b * np.dot(v, v))

    def simulate(self, N, v0=np.zeros(2)):
        """

        :param N: number of time steps
        :type N: int
        :param v0: initial velocity vector
        :type v0: ndarray
        :return: time series of velocity vectors with shape (N, v0.shape[0])
        :rtype: ndarray
        """
        v = [v0]
        n = N - 1
        gamma = np.random.randn(n, v0.size)
        for i in range(n):
            next_v = self.__call__(v[i]) + self.c * gamma[i]
            v.append(next_v)
        v_vec = np.array(v)
        return v_vec