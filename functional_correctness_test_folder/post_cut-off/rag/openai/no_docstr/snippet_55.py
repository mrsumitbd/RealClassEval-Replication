
import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        # No state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
                     Expected key: 'matrix' -> 2D list or np.ndarray of complex numbers.
        Returns:
            The solution in the format expected by the task:
            {
                'eigenvalues': list of complex numbers,
                'eigenvectors': list of lists (each inner list is a complex vector)
            }
        '''
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dictionary")
        if 'matrix' not in problem:
            raise KeyError("problem dictionary must contain 'matrix' key")

        mat = np.array(problem['matrix'], dtype=complex)
        if mat.ndim != 2 or mat.shape[0] != mat.shape[1]:
            raise ValueError("'matrix' must be a square 2D array")

        eigenvalues, eigenvectors = np.linalg.eig(mat)

        # Convert to Python lists for JSON serializability
        eigenvalues_list = [complex(val) for val in eigenvalues]
        eigenvectors_list = [[complex(val) for val in vec]
                             for vec in eigenvectors.T]

        return {
            'eigenvalues': eigenvalues_list,
            'eigenvectors': eigenvectors_list
        }

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary.
            solution: The proposed solution dictionary.
        Returns:
            True if the solution is valid, False otherwise.
        '''
        # Basic sanity checks
        if not isinstance(solution, dict):
            return False
        if 'eigenvalues' not in solution or 'eigenvectors' not in solution:
            return False

        try:
            mat = np.array(problem['matrix'], dtype=complex)
        except Exception:
            return False

        eigenvalues = np.array(solution['eigenvalues'], dtype=complex)
        eigenvectors = np.array(solution['eigenvectors'], dtype=complex)

        # Eigenvectors should be column vectors; ensure shape matches
        if eigenvectors.ndim != 2 or eigenvectors.shape[0] != mat.shape[0]:
            return False
        if eigenvectors.shape[1] != eigenvalues.shape[0]:
            return False

        # Verify each eigenpair: A v ≈ λ v
        tol = 1e-6
        for idx, (lam, vec) in enumerate(zip(eigenvalues, eigenvectors.T)):
            # Normalize vector to avoid scaling issues
            if np.linalg.norm(vec) == 0:
                return False
            vec_norm = vec / np.linalg.norm(vec)
            lhs = mat @ vec_norm
            rhs = lam * vec_norm
            if not np.allclose(lhs, rhs, atol=tol, rtol=tol):
                return False

        # Optionally, check that eigenvalues match (within tolerance)
        # Compute eigenvalues from matrix and compare sorted lists
        try:
            true_vals, _ = np.linalg.eig(mat)
        except Exception:
            return False
        if not np.allclose(np.sort(eigenvalues), np.sort(true_vals), atol=tol, rtol=tol):
            return False

        return True
