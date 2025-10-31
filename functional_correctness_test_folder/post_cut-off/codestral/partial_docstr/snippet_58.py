
import numpy as np


class LUFactorization:

    def __init__(self):

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

        # Perform LU factorization
        P, L, U = scipy.linalg.lu(A)

        # Solve the system of equations
        y = np.linalg.solve(L, np.dot(P, b))
        x = np.linalg.solve(U, y)

        return x

    def is_solution(self, problem, solution):

        A = problem['A']
        b = problem['b']

        # Check if the solution satisfies the equation Ax = b
        return np.allclose(np.dot(A, solution), b)
