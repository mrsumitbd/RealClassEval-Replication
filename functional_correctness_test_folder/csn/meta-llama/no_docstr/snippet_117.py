
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve_banded


class PDE:

    def __init__(self, lhs, rhs, bcs):
        """
        Initialize the PDE solver.

        Parameters:
        lhs (function): Left-hand side of the PDE, returns the coefficients of the finite difference equation.
        rhs (function): Right-hand side of the PDE, returns the value of the RHS at a given point.
        bcs (tuple): Boundary conditions, (left_bc, right_bc).
        """
        self.lhs = lhs
        self.rhs = rhs
        self.bcs = bcs

    def solve(self, N=100, L=1.0):
        """
        Solve the PDE using finite differences.

        Parameters:
        N (int): Number of grid points.
        L (float): Length of the domain.

        Returns:
        x (numpy array): Grid points.
        u (numpy array): Solution at the grid points.
        """
        x = np.linspace(0, L, N)
        h = x[1] - x[0]

        # Create the banded matrix for the LHS
        A = np.zeros((3, N))
        for i in range(N):
            A[:, i] = self.lhs(x[i], h)

        # Apply boundary conditions to the matrix
        A[1, 0] = 1
        A[0, 1] = 0
        A[2, 0] = 0
        A[1, -1] = 1
        A[0, -1] = 0
        A[2, -2] = 0

        # Create the RHS vector
        b = np.zeros(N)
        for i in range(N):
            b[i] = self.rhs(x[i])
        b[0] = self.bcs[0]
        b[-1] = self.bcs[1]

        # Solve the system
        u = solve_banded((1, 1), A, b)

        return x, u

# Example usage:


def lhs(x, h):
    return np.array([-1 / h**2, 2 / h**2, -1 / h**2])


def rhs(x):
    return np.sin(np.pi * x)


pde = PDE(lhs, rhs, (0, 0))
x, u = pde.solve(N=100, L=1.0)

plt.plot(x, u)
plt.show()
