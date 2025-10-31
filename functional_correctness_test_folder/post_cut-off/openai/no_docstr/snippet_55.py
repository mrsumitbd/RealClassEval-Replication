
import numpy as np


class EigenvectorsComplex:
    """
    A simple solver for eigenvectors of a complex square matrix.
    The `problem` argument is expected to provide a `matrix` attribute
    (or key) containing a 2‑D numpy array or list of lists.
    """

    def __init__(self):
        # No state needed for this stateless solver
        pass

    def _get_matrix(self, problem):
        """
        Extract the matrix from the problem. Supports either a dict-like
        object with a 'matrix' key or an object with a 'matrix' attribute.
        """
        if isinstance(problem, dict):
            matrix = problem.get("matrix")
        else:
            matrix = getattr(problem, "matrix", None)
        if matrix is None:
            raise ValueError(
                "Problem must provide a 'matrix' attribute or key.")
        return np.asarray(matrix, dtype=complex)

    def solve(self, problem):
        """
        Compute eigenvalues and eigenvectors of the matrix in `problem`.

        Returns:
            dict: {
                'eigenvalues': np.ndarray of shape (n,),
                'eigenvectors': np.ndarray of shape (n, n)  # columns are eigenvectors
            }
        """
        A = self._get_matrix(problem)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Matrix must be square.")
        eigenvalues, eigenvectors = np.linalg.eig(A)
        return {"eigenvalues": eigenvalues, "eigenvectors": eigenvectors}

    def is_solution(self, problem, solution):
        """
        Verify that `solution` is a valid set of eigenvectors for the matrix
        in `problem`. `solution` should be an array-like of shape (n, n)
        where each column is an eigenvector.

        Returns:
            bool: True if all columns are eigenvectors of the matrix,
                  False otherwise.
        """
        A = self._get_matrix(problem)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            return False

        # Ensure solution is a 2-D array
        try:
            sol = np.asarray(solution, dtype=complex)
        except Exception:
            return False

        if sol.ndim != 2 or sol.shape[0] != A.shape[0]:
            return False

        # Check each column
        for col in sol.T:
            # Skip zero vector
            if np.allclose(col, 0):
                return False
            # Compute A * v
            Av = A @ col
            # Check if Av is proportional to v
            # Find ratio using first non-zero component
            idx = np.argmax(np.abs(col))
            if np.abs(col[idx]) < 1e-12:
                return False
            ratio = Av[idx] / col[idx]
            if not np.allclose(Av, ratio * col, atol=1e-8, rtol=1e-5):
                return False
        return True
