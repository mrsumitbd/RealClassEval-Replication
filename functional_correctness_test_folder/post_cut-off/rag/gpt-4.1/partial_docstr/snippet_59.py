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
        # Expecting problem to have a key 'X' with a symmetric matrix to project
        X = np.array(problem['X'])
        # Ensure symmetry
        X_sym = (X + X.T) / 2
        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(X_sym)
        # Project: set negative eigenvalues to zero
        eigvals_proj = np.clip(eigvals, 0, None)
        # Reconstruct the matrix
        X_proj = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T
        # Ensure symmetry again due to numerical errors
        X_proj = (X_proj + X_proj.T) / 2
        return {'X_proj': X_proj}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        X_proj = np.array(solution['X_proj'])
        # Check symmetry
        if not np.allclose(X_proj, X_proj.T, atol=1e-8):
            return False
        # Check positive semidefiniteness: all eigenvalues >= 0
        eigvals = np.linalg.eigvalsh(X_proj)
        if np.all(eigvals >= -1e-8):
            return True
        return False
