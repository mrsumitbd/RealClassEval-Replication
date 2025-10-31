
import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        self._tolerance = 1e-8

    def solve(self, problem):
        """
        Compute eigenvalues and eigenvectors for a complex matrix.

        Parameters
        ----------
        problem : dict
            Must contain the key 'matrix' with a 2-D numpy array (complex or real).
            Optionally may contain 'eigenvalues' to compare against.

        Returns
        -------
        dict
            Dictionary with keys:
                'eigenvalues' : 1-D array of eigenvalues
                'eigenvectors' : 2-D array where columns are eigenvectors
        """
        if not isinstance(problem, dict):
            raise TypeError(
                "problem must be a dict containing at least the key 'matrix'")
        if 'matrix' not in problem:
            raise KeyError("problem dict must contain 'matrix' key")

        A = np.asarray(problem['matrix'])
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("'matrix' must be a square 2-D array")

        # Compute eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(A)

        result = {
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors
        }

        # If the problem supplied expected eigenvalues, store them for later validation
        if 'eigenvalues' in problem:
            result['expected_eigenvalues'] = np.asarray(problem['eigenvalues'])

        return result

    def is_solution(self, problem, solution):
        """
        Check if the provided solution is valid.

        Parameters
        ----------
        problem : dict
            Original problem dict containing at least 'matrix'.
        solution : dict
            Output from solve() containing 'eigenvalues' and 'eigenvectors'.

        Returns
        -------
        bool
            True if the solution is valid, False otherwise.
        """
        # Basic sanity checks
        if not isinstance(solution, dict):
            return False
        if 'eigenvalues' not in solution or 'eigenvectors' not in solution:
            return False

        A = np.asarray(problem['matrix'])
        eigvals = np.asarray(solution['eigenvalues'])
        eigvecs = np.asarray(solution['eigenvectors'])

        # Check shapes
        if eigvecs.shape[0] != A.shape[0]:
            return False
        if eigvecs.shape[1] != eigvals.size:
            return False

        # Verify each eigenpair: A @ v ≈ λ v
        for i in range(eigvals.size):
            v = eigvecs[:, i]
            λ = eigvals[i]
            residual = np.linalg.norm(A @ v - λ * v)
            if residual > self._tolerance * (np.linalg.norm(A @ v) + np.linalg.norm(λ * v)):
                return False

        # If expected eigenvalues were provided, compare them
        if 'expected_eigenvalues' in solution:
            expected = solution['expected_eigenvalues']
            # Sort both arrays for comparison
            if not np.allclose(np.sort(eigvals), np.sort(expected), atol=self._tolerance):
                return False

        return True
