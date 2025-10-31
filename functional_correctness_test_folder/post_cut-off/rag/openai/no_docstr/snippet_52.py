
import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PSDConeProjection.'''
        # No internal state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
                     Expected to contain a key 'matrix' with a square numpy array.
        Returns:
            The projected matrix (numpy.ndarray) that is the nearest PSD matrix
            to the input matrix in Frobenius norm.
        '''
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dictionary")
        if 'matrix' not in problem:
            raise KeyError("problem dictionary must contain 'matrix' key")
        A = problem['matrix']
        if not isinstance(A, np.ndarray):
            raise TypeError("'matrix' must be a numpy.ndarray")
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("'matrix' must be a square matrix")
        # Ensure symmetry
        A_sym = (A + A.T) / 2.0
        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(A_sym)
        # Zero out negative eigenvalues
        eigvals_clipped = np.clip(eigvals, a_min=0, a_max=None)
        # Reconstruct projected matrix
        projected = eigvecs @ np.diag(eigvals_clipped) @ eigvecs.T
        # Ensure symmetry numerically
        projected = (projected + projected.T) / 2.0
        return projected

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary.
            solution: The proposed solution (numpy.ndarray).
        Returns:
            True if the solution is valid, False otherwise.
        '''
        try:
            projected = self.solve(problem)
        except Exception:
            return False
        # Check symmetry
        if not isinstance(solution, np.ndarray):
            return False
        if solution.ndim != 2 or solution.shape[0] != solution.shape[1]:
            return False
        if not np.allclose(solution, solution.T, atol=1e-8):
            return False
        # Check PSD: eigenvalues non-negative within tolerance
        eigvals, _ = np.linalg.eigh(solution)
        if np.any(eigvals < -1e-8):
            return False
        # Check closeness to the true projection
        if not np.allclose(solution, projected, atol=1e-6):
            return False
        return True
