
import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PSDConeProjection.'''
        pass

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
                     Expected to contain key 'X' with a square numpy array.
        Returns:
            The projected matrix onto the PSD cone.
        '''
        X = problem.get('X')
        if X is None:
            raise ValueError(
                "Problem dictionary must contain key 'X' with a matrix.")
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        if X.ndim != 2 or X.shape[0] != X.shape[1]:
            raise ValueError("Input matrix X must be square.")
        # Ensure symmetry
        X_sym = (X + X.T) / 2.0
        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(X_sym)
        # Zero out negative eigenvalues
        eigvals_proj = np.clip(eigvals, a_min=0, a_max=None)
        # Reconstruct projected matrix
        X_proj = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T
        # Ensure symmetry numerically
        X_proj = (X_proj + X_proj.T) / 2.0
        return X_proj

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary.
            solution: The proposed solution matrix.
        Returns:
            True if the solution is valid, False otherwise.
        '''
        X = problem.get('X')
        if X is None:
            return False
        if not isinstance(solution, np.ndarray):
            return False
        if solution.shape != X.shape:
            return False
        # Check symmetry
        if not np.allclose(solution, solution.T, atol=1e-8):
            return False
        # Check PSD: all eigenvalues >= -tol
        eigvals = np.linalg.eigvalsh(solution)
        if np.any(eigvals < -1e-8):
            return False
        # Check that solution is the projection (within tolerance)
        X_proj = self.solve(problem)
        if not np.allclose(solution, X_proj, atol=1e-6):
            return False
        return True
