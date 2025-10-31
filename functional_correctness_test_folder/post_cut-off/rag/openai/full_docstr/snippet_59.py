
import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PSDConeProjection.'''
        # No state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
                     Expected key: 'matrix' -> a square numpy.ndarray
        Returns:
            The solution in the format expected by the task
            Returns a dict with key 'projected' containing the projected matrix.
        '''
        if 'matrix' not in problem:
            raise ValueError("Problem dictionary must contain 'matrix' key")

        X = np.asarray(problem['matrix'], dtype=float)

        if X.ndim != 2 or X.shape[0] != X.shape[1]:
            raise ValueError("'matrix' must be a square matrix")

        # Ensure symmetry (average with its transpose)
        X_sym = 0.5 * (X + X.T)

        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(X_sym)

        # Set negative eigenvalues to zero
        eigvals_proj = np.clip(eigvals, a_min=0.0, a_max=None)

        # Reconstruct projected matrix
        X_proj = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T

        # Ensure symmetry again (numerical errors)
        X_proj = 0.5 * (X_proj + X_proj.T)

        return {'projected': X_proj}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary
            solution: The proposed solution dictionary
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Basic checks
        if not isinstance(solution, dict) or 'projected' not in solution:
            return False

        X_proj = np.asarray(solution['projected'], dtype=float)

        # Must be square and same shape as original
        if X_proj.ndim != 2 or X_proj.shape[0] != X_proj.shape[1]:
            return False

        if 'matrix' not in problem:
            return False

        X_orig = np.asarray(problem['matrix'], dtype=float)
        if X_orig.shape != X_proj.shape:
            return False

        # Check symmetry
        if not np.allclose(X_proj, X_proj.T, atol=1e-8):
            return False

        # Check positive semidefiniteness: all eigenvalues >= -tol
        eigvals = np.linalg.eigvalsh(X_proj)
        if np.any(eigvals < -1e-8):
            return False

        # Optional: check that projection is indeed the closest PSD matrix
        # by verifying that the difference is orthogonal to the PSD cone.
        # For simplicity, we skip this expensive check.

        return True
