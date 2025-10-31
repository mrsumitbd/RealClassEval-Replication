
import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        pass

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
        Returns:
            The solution in the format expected by the task
        '''
        # Expecting problem['matrix'] as a list of lists (possibly with complex numbers)
        A = np.array(problem['matrix'], dtype=complex)
        # Compute eigenvalues and right eigenvectors
        vals, vecs = np.linalg.eig(A)
        # Return as list of lists (each column is an eigenvector)
        # Transpose to get eigenvectors as rows
        eigenvectors = [vecs[:, i].tolist() for i in range(vecs.shape[1])]
        return eigenvectors

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        A = np.array(problem['matrix'], dtype=complex)
        # Compute eigenvalues and eigenvectors
        vals, vecs = np.linalg.eig(A)
        # For each provided eigenvector, check if it is an eigenvector of A
        for v in solution:
            v = np.array(v, dtype=complex)
            if v.shape[0] != A.shape[0]:
                return False
            # Check if Av = lambda v for some eigenvalue lambda
            Av = A @ v
            # Try to find a scalar lambda such that Av ≈ lambda*v
            # Avoid division by zero
            nonzero_idx = np.where(np.abs(v) > 1e-8)[0]
            if len(nonzero_idx) == 0:
                return False
            ratios = Av[nonzero_idx] / v[nonzero_idx]
            # All ratios should be (approximately) equal
            if not np.allclose(ratios, ratios[0], atol=1e-6):
                return False
        return True
