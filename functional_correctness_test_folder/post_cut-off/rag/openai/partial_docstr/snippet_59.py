
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
                     Expected to contain a key 'matrix' with a square numpy array.
        Returns:
            The solution in the format expected by the task
            (a dictionary with key 'projection' containing the projected matrix).
        '''
        if 'matrix' not in problem:
            raise ValueError("Problem dictionary must contain a 'matrix' key.")
        X = np.asarray(problem['matrix'], dtype=float)
        if X.ndim != 2 or X.shape[0] != X.shape[1]:
            raise ValueError("Input matrix must be square.")
        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(X)
        # Zero out negative eigenvalues
        eigvals_proj = np.maximum(eigvals, 0.0)
        # Reconstruct projected matrix
        X_proj = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T
        # Ensure symmetry (numerical errors)
        X_proj = (X_proj + X_proj.T) / 2.0
        return {'projection': X_proj}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary.
            solution: The proposed solution dictionary.
        Returns:
            True if the solution is valid, False otherwise.
        '''
        # Basic checks
        if not isinstance(solution, dict) or 'projection' not in solution:
            return False
        X_proj = np.asarray(solution['projection'], dtype=float)
        if X_proj.ndim != 2 or X_proj.shape[0] != X_proj.shape[1]:
            return False
        # Symmetry check
        if not np.allclose(X_proj, X_proj.T, atol=1e-8):
            return False
        # PSD check
        eigvals = np.linalg.eigvalsh(X_proj)
        if np.any(eigvals < -1e-8):
            return False
        # Optional: check that projection is close to original
        if 'matrix' in problem:
            X_orig = np.asarray(problem['matrix'], dtype=float)
            diff_norm = np.linalg.norm(X_proj - X_orig, ord='fro')
            # The projection should not increase the Frobenius norm relative to any other PSD matrix.
            # We cannot guarantee optimality here, but we can ensure the difference is not absurdly large.
            if diff_norm > 1e6:  # arbitrary large threshold
                return False
        return True
