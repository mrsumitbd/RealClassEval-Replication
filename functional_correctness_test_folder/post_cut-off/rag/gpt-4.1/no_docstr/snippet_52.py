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
        Returns:
            The solution in the format expected by the task
        '''
        # Assume problem contains a symmetric matrix 'A'
        A = np.array(problem['A'])
        # Project A onto the PSD cone: set negative eigenvalues to zero
        eigvals, eigvecs = np.linalg.eigh(A)
        eigvals_proj = np.clip(eigvals, 0, None)
        A_proj = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T
        # Ensure symmetry
        A_proj = (A_proj + A_proj.T) / 2
        return {'X': A_proj}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        X = np.array(solution['X'])
        # Check symmetry
        if not np.allclose(X, X.T, atol=1e-8):
            return False
        # Check positive semidefiniteness: all eigenvalues >= 0
        eigvals = np.linalg.eigvalsh(X)
        if np.any(eigvals < -1e-8):
            return False
        return True
