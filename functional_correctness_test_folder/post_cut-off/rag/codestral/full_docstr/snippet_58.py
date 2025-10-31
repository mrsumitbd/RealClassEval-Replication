
import numpy as np


class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        self.L = None
        self.U = None
        self.P = None

    def solve(self, problem):
        '''
        Solve the lu_factorization problem.
        Args:
            problem: Dictionary containing problem data specific to lu_factorization
        Returns:
            The solution in the format expected by the task
        '''
        A = problem.get('matrix')
        if A is None:
            raise ValueError(
                "Problem must contain a 'matrix' key with the input matrix.")

        A = np.array(A, dtype=float)
        P, L, U = self._lu_factorization(A)

        self.L = L
        self.U = U
        self.P = P

        return {
            'L': L.tolist(),
            'U': U.tolist(),
            'P': P.tolist()
        }

    def _lu_factorization(self, A):
        '''Perform LU factorization with partial pivoting.'''
        n = A.shape[0]
        L = np.eye(n, dtype=float)
        U = A.copy()
        P = np.eye(n, dtype=float)

        for k in range(n - 1):
            # Partial pivoting
            max_index = np.argmax(np.abs(U[k:, k])) + k
            if max_index != k:
                U[[k, max_index]] = U[[max_index, k]]
                P[[k, max_index]] = P[[max_index, k]]
                if k >= 1:
                    L[[k, max_index], :k] = L[[max_index, k], :k]

            # Check for singularity
            if np.abs(U[k, k]) < 1e-10:
                raise ValueError("Matrix is singular or nearly singular.")

            for i in range(k + 1, n):
                factor = U[i, k] / U[k, k]
                L[i, k] = factor
                U[i, k:] -= factor * U[k, k:]

        return P, L, U

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        A = np.array(problem.get('matrix'))
        L = np.array(solution.get('L'))
        U = np.array(solution.get('U'))
        P = np.array(solution.get('P'))

        if L is None or U is None or P is None:
            return False

        # Check if PA = LU
        PA = np.dot(P, A)
        LU = np.dot(L, U)

        return np.allclose(PA, LU, atol=1e-10)
