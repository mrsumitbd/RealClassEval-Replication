
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
            The projected matrix onto the PSD cone.
        '''
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dict")
        if 'matrix' not in problem:
            raise KeyError("problem dict must contain 'matrix' key")
        X = problem['matrix']
        if not isinstance(X, np.ndarray):
            raise TypeError("'matrix' must be a numpy.ndarray")
        if X.ndim != 2 or X.shape[0] != X.shape[1]:
            raise ValueError("'matrix' must be square")
        # Symmetrize to avoid numerical asymmetry
        X_sym = (X + X.T) / 2.0
        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(X_sym)
        # Zero out negative eigenvalues
        eigvals_proj = np.clip(eigvals, a_min=0.0, a_max=None)
        # Reconstruct projected matrix
        X_proj = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T
        # Ensure symmetry
        X_proj = (X_proj + X_proj.T) / 2.0
        return X_proj

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dict (must contain 'matrix')
            solution: The proposed solution matrix (numpy array)
        Returns:
            True if the solution is symmetric, PSD, and close to the projection
            of the original matrix; False otherwise.
        '''
        if not isinstance(solution, np.ndarray):
            return False
        if solution.ndim != 2 or solution.shape[0] != solution.shape[1]:
            return False
        # Check symmetry
        if not np.allclose(solution, solution.T, atol=1e-8):
            return False
        # Check PSD: all eigenvalues >= -tol
        eigvals = np.linalg.eigvalsh(solution)
        if np.any(eigvals < -1e-8):
            return False
        # Optional: check that solution is the projection of the original
        try:
            X_proj = self.solve(problem)
        except Exception:
            return False
        # Compare with tolerance
        return np.allclose(solution, X_proj, atol=1e-6)
