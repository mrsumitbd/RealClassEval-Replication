
import numpy as np


class PDE:
    """
    A very simple 1‑D heat‑equation solver using an explicit finite‑difference scheme.
    The constructor accepts the left‑hand side (lhs) and right‑hand side (rhs) functions
    of the PDE, boundary conditions (bcs), and optional discretisation parameters.
    """

    def __init__(self, lhs, rhs, bcs,
                 domain=(0.0, 1.0), nx=51, dt=1e-4, t_final=0.01):
        """
        Parameters
        ----------
        lhs : callable
            Function representing the left‑hand side of the PDE. For the heat
            equation this is typically ``u_t``. It is not used directly in the
            solver but kept for compatibility with the interface.
        rhs : callable
            Function representing the spatial part of the PDE. For the heat
            equation this is typically ``u_xx``. It is expected to accept a
            1‑D numpy array of spatial points and return the initial condition
            for the temperature field.
        bcs : dict
            Boundary conditions. Expected keys are ``'left'`` and ``'right'``.
            The values are the Dirichlet boundary values at the left and right
            ends of the domain.
        domain : tuple of float, optional
            Spatial domain as (x_start, x_end).
        nx : int, optional
            Number of spatial grid points.
        dt : float, optional
            Time step size.
        t_final : float, optional
            Final time to integrate to.
        """
        self.lhs = lhs
        self.rhs = rhs
        self.bcs = bcs
        self.domain = domain
        self.nx = nx
        self.dt = dt
        self.t_final = t_final

    def solve(self):
        """
        Solve the PDE using an explicit finite‑difference scheme.

        Returns
        -------
        x : numpy.ndarray
            Spatial grid points.
        u : numpy.ndarray
            Solution at the final time.
        """
        x_start, x_end = self.domain
        L = x_end - x_start
        dx = L / (self.nx - 1)

        # Initial condition from rhs (interpreted as u(x,0))
        x = np.linspace(x_start, x_end, self.nx)
        u = self.rhs(x)

        # Apply Dirichlet boundary conditions
        u[0] = self.bcs.get('left', 0.0)
        u[-1] = self.bcs.get('right', 0.0)

        # Stability condition for explicit scheme (alpha = 1)
        alpha = 1.0
        if alpha * self.dt / dx**2 > 0.5:
            raise ValueError(
                "Time step too large for stability (dt > 0.5*dx^2).")

        nt = int(np.ceil(self.t_final / self.dt))
        for _ in range(nt):
            u_new = u.copy()
            for i in range(1, self.nx - 1):
                u_new[i] = u[i] + alpha * self.dt / dx**2 * (
                    u[i + 1] - 2 * u[i] + u[i - 1]
                )
            # Re‑apply boundary conditions
            u_new[0] = self.bcs.get('left', 0.0)
            u_new[-1] = self.bcs.get('right', 0.0)
            u = u_new

        return x, u
