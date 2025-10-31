
import numpy as np


class LUFactorization:

    def __init__(self):
        self.lower_triangular = None
        self.upper_triangular = None

    def solve(self, problem):
        """
        Solves a system of linear equations using LU factorization.

        Args:
        problem (dict): A dictionary containing the coefficient matrix 'A' and the constant vector 'b'.

        Returns:
        solution (numpy array): The solution to the system of linear equations.
        """
        A = problem['A']
        b = problem['b']

        # Perform LU factorization
        self.lower_triangular, self.upper_triangular = self._lu_factorization(
            A)

        # Solve the system using the LU factorization
        y = self._forward_substitution(self.lower_triangular, b)
        solution = self._backward_substitution(self.upper_triangular, y)

        return solution

    def is_solution(self, problem, solution):
        """
        Checks if a given solution satisfies a system of linear equations.

        Args:
        problem (dict): A dictionary containing the coefficient matrix 'A' and the constant vector 'b'.
        solution (numpy array): The proposed solution to the system of linear equations.

        Returns:
        bool: True if the solution satisfies the system, False otherwise.
        """
        A = problem['A']
        b = problem['b']

        # Check if the solution satisfies the system
        residual = np.dot(A, solution) - b
        return np.allclose(residual, np.zeros_like(residual))

    def _lu_factorization(self, A):
        """
        Performs LU factorization on a given matrix.

        Args:
        A (numpy array): The matrix to be factorized.

        Returns:
        L (numpy array): The lower triangular matrix.
        U (numpy array): The upper triangular matrix.
        """
        n = A.shape[0]
        L = np.eye(n)
        U = np.copy(A)

        for i in range(n - 1):
            for j in range(i + 1, n):
                factor = U[j, i] / U[i, i]
                L[j, i] = factor
                U[j, :] -= factor * U[i, :]

        return L, U

    def _forward_substitution(self, L, b):
        """
        Solves a lower triangular system using forward substitution.

        Args:
        L (numpy array): The lower triangular matrix.
        b (numpy array): The constant vector.

        Returns:
        y (numpy array): The solution to the lower triangular system.
        """
        n = L.shape[0]
        y = np.zeros(n)

        for i in range(n):
            y[i] = (b[i] - np.dot(L[i, :i], y[:i])) / L[i, i]

        return y

    def _backward_substitution(self, U, y):
        """
        Solves an upper triangular system using backward substitution.

        Args:
        U (numpy array): The upper triangular matrix.
        y (numpy array): The constant vector.

        Returns:
        x (numpy array): The solution to the upper triangular system.
        """
        n = U.shape[0]
        x = np.zeros(n)

        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - np.dot(U[i, i + 1:], x[i + 1:])) / U[i, i]

        return x


# Example usage:
if __name__ == "__main__":
    # Define a problem
    A = np.array([[4, 3], [6, 3]])
    b = np.array([10, 12])
    problem = {'A': A, 'b': b}

    # Create an instance of the LUFactorization class
    lu_factorization = LUFactorization()

    # Solve the problem
    solution = lu_factorization.solve(problem)
    print("Solution:", solution)

    # Check if the solution is correct
    is_correct = lu_factorization.is_solution(problem, solution)
    print("Is solution correct?", is_correct)
