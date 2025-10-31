
import numpy as np


class PSDConeProjection:
    """
    Projection of a symmetric matrix onto the positive semidefinite (PSD) cone.
    """

    def __init__(self):
        """
        No special initialization required.
        """
        pass

    def solve(self, problem):
        """
        Project the matrix contained in `problem` onto the PSD cone.

        Parameters
        ----------
        problem : object or dict
            Must contain a symmetric matrix under the key/attribute `matrix`.
            Optionally may contain a tolerance under `tolerance`.

        Returns
        -------
        projected : ndarray
            The projection of the input matrix onto the PSD cone.
        """
        # Extract matrix
        if isinstance(problem, dict):
            A = problem.get("matrix")
            tol = problem.get("tolerance", 1e-8)
        else:
            A = getattr(problem, "matrix", None)
            tol = getattr(problem, "tolerance", 1e-8)

        if A is None:
            raise ValueError(
                "Problem must contain a 'matrix' attribute or key.")

        A = np.asarray(A, dtype=float)

        # Ensure symmetry (within tolerance)
        if not np.allclose(A, A.T, atol=tol):
            raise ValueError("Input matrix must be symmetric.")

        # Eigenvalue decomposition
        eigvals, eigvecs = np.linalg.eigh(A)

        # Zero out negative eigenvalues
        eigvals_proj = np.maximum(eigvals, 0.0)

        # Reconstruct projected matrix
        projected = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T

        # Ensure symmetry numerically
        projected = (projected + projected.T) / 2.0

        return projected

    def is_solution(self, problem, solution):
        """
        Verify that `solution` is a valid PSD projection of the matrix in `problem`.

        Parameters
        ----------
        problem : object or dict
            Must contain the original matrix under the key/attribute `matrix`.
        solution : ndarray
            Candidate projected matrix.

        Returns
        -------
        bool
            True if `solution` is symmetric, PSD (within tolerance) and close to the
            projection of the original matrix.
        """
        # Extract matrix and tolerance
        if isinstance(problem, dict):
            A = problem.get("matrix")
            tol = problem.get("tolerance", 1e-8)
        else:
            A = getattr(problem, "matrix", None)
            tol = getattr(problem, "tolerance", 1e-8)

        if A is None:
            raise ValueError(
                "Problem must contain a 'matrix' attribute or key.")

        A = np.asarray(A, dtype=float)
        solution = np.asarray(solution, dtype=float)

        # Check shapes
        if A.shape != solution.shape:
            return False

        # Check symmetry of solution
        if not np.allclose(solution, solution.T, atol=tol):
            return False

        # Check PSD: all eigenvalues >= -tol
        eigvals = np.linalg.eigvalsh(solution)
        if np.any(eigvals < -tol):
            return False

        # Check closeness to the true projection
        projected_true = self.solve(problem)
        if not np.allclose(solution, projected_true, atol=tol):
            return False

        return True
