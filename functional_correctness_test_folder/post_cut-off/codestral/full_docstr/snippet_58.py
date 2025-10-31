
import numpy as np


class LUFactorization:

    def __init__(self):
        '''Initialize the LUFactorization.'''
        pass

    def solve(self, problem):
        '''
        Solve the lu_factorization problem.
        Args:
            problem: Dictionary containing problem data specific to lu_factorization
        Returns:
            The solution in the format expected by the task
        '''
        A = problem['A']
        b = problem['b']
        P, L, U = self.lu_factorization(A)
        y = self.forward_substitution(L, P.dot(b))
        x = self.backward_substitution(U, y)
        return {'x': x, 'P': P, 'L': L, 'U': U}

    def lu_factorization(self, A):
        '''
        Perform LU factorization on matrix A.
        Args:
            A: The matrix to factorize
        Returns:
            P: Permutation matrix
            L: Lower triangular matrix
            U: Upper triangular matrix
        '''
        n = A.shape[0]
        P = np.eye(n)
        L = np.zeros((n, n))
        U = np.zeros((n, n))

        for k in range(n):
            # Partial pivoting
            max_row = np.argmax(np.abs(A[k:, k])) + k
            if max_row != k:
                A[[k, max_row]] = A[[max_row, k]]
                P[[k, max_row]] = P[[max_row, k]]

            L[k, k] = 1
            U[k, :] = A[k, :]

            for i in range(k+1, n):
                L[i, k] = A[i, k] / U[k, k]
                U[i, k:] = A[i, k:] - L[i, k] * U[k, k:]

        return P, L, U

    def forward_substitution(self, L, b):
        '''
        Solve Ly = b for y using forward substitution.
        Args:
            L: Lower triangular matrix
            b: Right-hand side vector
        Returns:
            y: Solution vector
        '''
        n = L.shape[0]
        y = np.zeros(n)

        for i in range(n):
            y[i] = (b[i] - np.dot(L[i, :i], y[:i])) / L[i, i]

        return y

    def backward_substitution(self, U, y):
        '''
        Solve Ux = y for x using backward substitution.
        Args:
            U: Upper triangular matrix
            y: Right-hand side vector
        Returns:
            x: Solution vector
        '''
        n = U.shape[0]
        x = np.zeros(n)

        for i in range(n-1, -1, -1):
            x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]

        return x

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        A = problem['A']
        b = problem['b']
        x = solution['x']
        P = solution['P']
        L = solution['L']
        U = solution['U']

        # Check if A = P*L*U
        if not np.allclose(A, P.dot(L).dot(U)):
            return False

        # Check if x is a solution to Ax = b
        if not np.allclose(A.dot(x), b):
            return False

        return True
