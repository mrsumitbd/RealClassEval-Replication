
import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self, tol=1e-8):
        """
        Parameters
        ----------
        tol : float, optional
            Tolerance for checking positive semidefiniteness and symmetry.
        """
        self.tol = tol

    def solve(self, problem):
        """
        Project the matrix in `problem` onto the positive semidefinite cone.

        Parameters
        ----------
        problem : object
            Must have an attribute `matrix` which is a square numpy.ndarray.

        Returns
        -------
        numpy.ndarray
            The projected positive semidefinite matrix.
        """
        if not hasattr(problem, 'matrix'):
            raise AttributeError(
                "Problem object must have a 'matrix' attribute.")
        A = np.asarray(problem.matrix, dtype=float)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Input matrix must be square.")
        # Symmetrize to avoid numerical asymmetry
        A_sym = (A + A.T) / 2.0
        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(A_sym)
        # Zero out negative eigenvalues
        eigvals_proj = np.clip(eigvals, a_min=0.0, a_max=None)
        # Reconstruct
        A_proj = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T
        # Ensure symmetry
        A_proj = (A_proj + A_proj.T) / 2.0
        return A_proj

    def is_solution(self, problem, solution):
        """
        Check whether `solution` is a valid PSD projection of `problem.matrix`.

        Parameters
        ----------
        problem : object
            Must have an attribute `matrix` which is a square numpy.ndarray.
        solution : numpy.ndarray
            The matrix to validate.

        Returns
        -------
        bool
            True if `solution` is symmetric, PSD, and close to the projection of
            `problem.matrix` within the specified tolerance.
        """
        if not hasattr(problem, 'matrix'):
            raise AttributeError(
                "Problem object must have a 'matrix' attribute.")
        A = np.asarray(problem.matrix, dtype=float)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Input matrix must be square.")
        if solution.ndim != 2 or solution.shape != A.shape:
            return False
        # Symmetry check
        if not np.allclose(solution, solution.T, atol=self.tol):
            return False
        # PSD check via eigenvalues
        eigvals = np.linalg.eigvalsh(solution)
        if np.any(eigvals < -self.tol):
            return False
        # Compare to projection
        proj = self.solve(problem)
        if not np.allclose(solution, proj, atol=self.tol):
            return False
        return True
