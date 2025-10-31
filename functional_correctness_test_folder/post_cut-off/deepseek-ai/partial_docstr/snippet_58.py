
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
        A = np.array(problem['A'])
        n = A.shape[0]
        L = np.eye(n)
        U = np.zeros((n, n))

        for i in range(n):
            for j in range(i, n):
                U[i, j] = A[i, j] - sum(L[i, k] * U[k, j] for k in range(i))
            for j in range(i + 1, n):
                L[j, i] = (A[j, i] - sum(L[j, k] * U[k, i]
                           for k in range(i))) / U[i, i]

        solution = {
            'L': L.tolist(),
            'U': U.tolist()
        }
        return solution

    def is_solution(self, problem, solution):
        A = np.array(problem['A'])
        L = np.array(solution['L'])
        U = np.array(solution['U'])
        reconstructed_A = np.dot(L, U)
        return np.allclose(A, reconstructed_A)
