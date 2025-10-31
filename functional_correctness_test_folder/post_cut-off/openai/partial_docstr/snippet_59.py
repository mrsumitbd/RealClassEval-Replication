
import numpy as np


class PSDConeProjection:
    """
    Project a symmetric matrix onto the positive semidefinite cone.
    """

    def __init__(self):
        # No initialization needed for this simple implementation
        pass

    def solve(self, problem):
        """
        Solve the psd_cone_projection problem.

        Parameters
        ----------
        problem : dict
            Dictionary containing problem data specific to psd_cone_projection.
            Expected key:
                - 'X': numpy.ndarray, symmetric matrix to be projected.

        Returns
        -------
        dict
            Dictionary containing the projected matrix under the key 'X_proj'.
        """
        if not isinstance(problem, dict):
            raise TypeError("Problem must be a dictionary.")
        if 'X' not in problem:
            raise KeyError("Problem dictionary must contain key 'X'.")

        X = problem['X']
        if not isinstance(X, np.ndarray):
            raise TypeError("X must be a numpy.ndarray.")
        if X.ndim != 2 or X.shape[0] != X.shape[1]:
            raise ValueError("X must be a square matrix.")

        # Ensure symmetry (average with its transpose)
        X_sym = 0.5 * (X + X.T)

        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(X_sym)

        # Zero out negative eigenvalues
        eigvals_proj = np.clip(eigvals, a_min=0, a_max=None)

        # Reconstruct the projected matrix
        X_proj = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T

        # Ensure symmetry numerically
        X_proj = 0.5 * (X_proj + X_proj.T)

        return {'X_proj': X_proj}

    def is_solution(self, problem, solution, atol=1e-8, rtol=1e-6):
        """
        Verify that the provided solution is a valid projection onto the PSD cone.

        Parameters
        ----------
        problem : dict
            Original problem dictionary containing key 'X'.
        solution : dict
            Dictionary returned by `solve`, expected to contain key 'X_proj'.
        atol : float, optional
            Absolute tolerance for numerical checks.
        rtol : float, optional
            Relative tolerance for numerical checks.

        Returns
        -------
        bool
            True if the solution satisfies the PSD projection properties, False otherwise.
        """
        # Basic type checks
        if not isinstance(solution, dict) or 'X_proj' not in solution:
            return False

        X = problem.get('X')
        X_proj = solution['X_proj']

        if X is None or X_proj is None:
            return False

        if not isinstance(X, np.ndarray) or not isinstance(X_proj, np.ndarray):
            return False

        # Check shapes
        if X.shape != X_proj.shape:
            return False

        # Check symmetry of X_proj
        if not np.allclose(X_proj, X_proj.T, atol=atol, rtol=rtol):
            return False

        # Check positive semidefiniteness: all eigenvalues >= -tol
        eigvals_proj = np.linalg.eigvalsh(X_proj)
        if np.any(eigvals_proj < -max(atol, rtol * np.abs(eigvals_proj).max())):
            return False

        # Optional: check that the projection is close to the original matrix
        # in Frobenius norm (within a tolerance). This is not strictly required
        # for a valid projection but helps catch trivial solutions.
        diff_norm = np.linalg.norm(X - X_proj, ord='fro')
        X_norm = np.linalg.norm(X, ord='fro')
        if diff_norm > max(atol, rtol * X_norm):
            return False

        return True
