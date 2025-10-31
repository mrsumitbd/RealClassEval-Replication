
import numpy as np


class EigenvectorsComplex:
    """
    Compute eigenvalues and eigenvectors of a complex square matrix.
    The `solve` method returns a list of (eigenvalue, eigenvector) tuples.
    The `is_solution` method verifies that each pair satisfies A v = λ v.
    """

    def __init__(self):
        # No initialization needed for this simple implementation
        pass

    def solve(self, problem):
        """
        Compute eigenvalues and eigenvectors for the given problem.

        Parameters
        ----------
        problem : object or dict
            Must provide a square complex matrix via `problem.matrix` or
            `problem['matrix']`.

        Returns
        -------
        list of tuples
            Each tuple is (eigenvalue, eigenvector) where eigenvector is a
            column vector (numpy.ndarray) of shape (n,).
        """
        # Extract the matrix
        if isinstance(problem, dict):
            matrix = problem.get('matrix')
        else:
            matrix = getattr(problem, 'matrix', None)

        if matrix is None:
            raise ValueError(
                "Problem must provide a 'matrix' attribute or key.")

        matrix = np.asarray(matrix, dtype=complex)

        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Matrix must be square.")

        # Compute eigenvalues and eigenvectors
        eigvals, eigvecs = np.linalg.eig(matrix)

        # Convert eigenvectors to 1-D arrays
        result = [(eigvals[i], eigvecs[:, i]) for i in range(len(eigvals))]
        return result

    def is_solution(self, problem, solution, atol=1e-8, rtol=1e-5):
        """
        Verify that the provided solution satisfies A v = λ v for each pair.

        Parameters
        ----------
        problem : object or dict
            Must provide the matrix as in `solve`.
        solution : list of tuples
            Output from `solve` or a user-provided list of (eigenvalue, eigenvector).
        atol, rtol : float
            Absolute and relative tolerances for the check.

        Returns
        -------
        bool
            True if all pairs satisfy the eigenvalue equation within tolerance.
        """
        # Extract the matrix
        if isinstance(problem, dict):
            matrix = problem.get('matrix')
        else:
            matrix = getattr(problem, 'matrix', None)

        if matrix is None:
            raise ValueError(
                "Problem must provide a 'matrix' attribute or key.")

        matrix = np.asarray(matrix, dtype=complex)

        if not isinstance(solution, list):
            return False

        for pair in solution:
            if not isinstance(pair, (tuple, list)) or len(pair) != 2:
                return False
            eigval, eigvec = pair
            eigvec = np.asarray(eigvec, dtype=complex)
            # Check dimensions
            if eigvec.ndim != 1 or eigvec.shape[0] != matrix.shape[0]:
                return False
            # Compute A v
            Av = matrix @ eigvec
            # Compute λ v
            lv = eigval * eigvec
            if not np.allclose(Av, lv, atol=atol, rtol=rtol):
                return False
        return True
