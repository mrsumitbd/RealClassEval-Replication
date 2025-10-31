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
        # Expecting problem to have a key 'matrix' with a 2D list or np.ndarray
        matrix = problem.get('matrix')
        if matrix is None:
            raise ValueError("Problem dictionary must contain 'matrix' key.")
        A = np.array(matrix, dtype=complex)
        vals, vecs = np.linalg.eig(A)
        # Return as a dict for clarity
        return {
            'eigenvalues': vals,
            'eigenvectors': vecs
        }

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        matrix = problem.get('matrix')
        if matrix is None:
            return False
        A = np.array(matrix, dtype=complex)
        vals = solution.get('eigenvalues')
        vecs = solution.get('eigenvectors')
        if vals is None or vecs is None:
            return False
        # Check shape
        if vecs.shape[0] != A.shape[0]:
            return False
        # Check that A @ v ≈ λ v for each eigenpair
        for i in range(len(vals)):
            v = vecs[:, i]
            lam = vals[i]
            Av = A @ v
            lv = lam * v
            if not np.allclose(Av, lv, atol=1e-6):
                return False
        return True
