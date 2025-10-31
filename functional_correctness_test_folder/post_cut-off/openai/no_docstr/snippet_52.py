
import numpy as np


class PSDConeProjection:
    """
    Projection of a symmetric matrix onto the positive semidefinite (PSD) cone.
    The projection is performed by eigenvalue decomposition: negative eigenvalues
    are set to zero and the matrix is reconstructed.
    """

    def __init__(self, tol: float = 1e-8):
        """
        Parameters
        ----------
        tol : float, optional
            Tolerance used for numerical checks (default 1e-8).
        """
        self.tol = tol

    def solve(self, problem):
        """
        Project the matrix in `problem` onto the PSD cone.

        Parameters
        ----------
        problem : dict
            Must contain a key 'matrix' with a NumPy array.

        Returns
        -------
        np.ndarray
            The projected PSD matrix.
        """
        if not isinstance(problem, dict) or 'matrix' not in problem:
            raise ValueError(
                "Problem must be a dict containing a 'matrix' key.")

        A = np.asarray(problem['matrix'], dtype=float)

        # Ensure the matrix is square
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Input matrix must be square.")

        # Symmetrize to avoid numerical asymmetry
        A_sym = (A + A.T) / 2.0

        # Eigenvalue decomposition
        eigvals, eigvecs = np.linalg.eigh(A_sym)

        # Zero out negative eigenvalues
        eigvals_proj = np.maximum(eigvals, 0.0)

        # Reconstruct the projected matrix
        A_proj = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T

        # Ensure symmetry after reconstruction
        A_proj = (A_proj + A_proj.T) / 2.0

        return A_proj

    def is_solution(self, problem, solution):
        """
        Verify that `solution` is a valid PSD projection of the matrix in `problem`.

        Parameters
        ----------
        problem : dict
            Must contain a key 'matrix' with a NumPy array.
        solution : np.ndarray
            The matrix to be verified.

        Returns
        -------
        bool
            True if `solution` is symmetric, PSD, and close to the projection of
            the original matrix within the specified tolerance.
        """
        if not isinstance(solution, np.ndarray):
            return False

        # Check symmetry
        if not np.allclose(solution, solution.T, atol=self.tol):
            return False

        # Check PSD: all eigenvalues non-negative within tolerance
        eigvals = np.linalg.eigvalsh(solution)
        if np.any(eigvals < -self.tol):
            return False

        # Compute the exact projection and compare
        try:
            proj = self.solve(problem)
        except Exception:
            return False

        # Check closeness
        return np.allclose(solution, proj, atol=self.tol)
