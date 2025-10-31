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
        # Expect problem to have key 'A' with a symmetric matrix to project
        A = np.array(problem['A'])
        # Ensure symmetry
        A = (A + A.T) / 2
        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(A)
        # Project: set negative eigenvalues to zero
        eigvals_proj = np.clip(eigvals, 0, None)
        # Reconstruct the matrix
        A_proj = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T
        # Ensure symmetry in output
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
