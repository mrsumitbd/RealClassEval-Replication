import numpy as np


class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

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
        A = np.array(problem['matrix'], dtype=float)
        n = A.shape[0]
        L = np.zeros((n, n), dtype=float)
        U = np.zeros((n, n), dtype=float)

        for i in range(n):
            # Upper Triangular
            for k in range(i, n):
                sum_ = sum(L[i][j] * U[j][k] for j in range(i))
                U[i][k] = A[i][k] - sum_
            # Lower Triangular
            L[i][i] = 1.0
            for k in range(i+1, n):
                sum_ = sum(L[k][j] * U[j][i] for j in range(i))
                if U[i][i] == 0:
                    raise ValueError("Zero pivot encountered.")
                L[k][i] = (A[k][i] - sum_) / U[i][i]

        return {
            'L': L.tolist(),
            'U': U.tolist()
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
        A = np.array(problem['matrix'], dtype=float)
        L = np.array(solution['L'], dtype=float)
        U = np.array(solution['U'], dtype=float)
        try:
            reconstructed = np.dot(L, U)
            return np.allclose(A, reconstructed)
        except Exception:
            return False
