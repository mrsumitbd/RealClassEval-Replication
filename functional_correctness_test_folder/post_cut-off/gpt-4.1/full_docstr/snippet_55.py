
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
        # Expecting problem['matrix'] as a list of lists (complex numbers allowed)
        A = np.array(problem['matrix'], dtype=complex)
        # Compute eigenvalues and right eigenvectors
        _, vecs = np.linalg.eig(A)
        # Return as list of lists (each column is an eigenvector)
        # Each eigenvector is a list of complex numbers
        return [vecs[:, i].tolist() for i in range(vecs.shape[1])]

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
        # Normalize eigenvectors for comparison

        def normalize(v):
            norm = np.linalg.norm(v)
            if norm == 0:
                return v
            return v / norm

        # For each provided solution vector, check if it's an eigenvector of A
        for sol_vec in solution:
            v = np.array(sol_vec, dtype=complex)
            if np.allclose(v, 0):
                return False
            v_norm = normalize(v)
            # Try to find a matching eigenvector from numpy's output
            found = False
            for i in range(vecs.shape[1]):
                eigvec = vecs[:, i]
                eigvec_norm = normalize(eigvec)
                # Eigenvectors can differ by a scalar multiple (including complex phase)
                # So check if they are colinear
                # v = alpha * eigvec, so v / eigvec = alpha (should be constant for all nonzero entries)
                # Instead, check if the angle between them is zero (up to a tolerance)
                if np.allclose(np.abs(np.vdot(v_norm, eigvec_norm)), 1, atol=1e-6):
                    found = True
                    break
            if not found:
                return False
        return True
