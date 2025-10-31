import numpy as np


class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        self.tol = 1e-8

    def _get_matrix_from_problem(self, problem):
        keys = ['A', 'matrix', 'mat', 'input', 'data']
        A = None
        for k in keys:
            if k in problem:
                A = problem[k]
                break
        if A is None:
            raise ValueError(
                'Problem does not contain a matrix under any of keys: {}'.format(keys))
        A = np.array(A, dtype=float)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError('Matrix must be square 2D array')
        return A

    def _lu_factorization_partial_pivot(self, A):
        n = A.shape[0]
        U = A.copy()
        L = np.eye(n, dtype=float)
        P = np.eye(n, dtype=float)

        for k in range(n):
            # Pivot selection
            pivot = np.argmax(np.abs(U[k:, k])) + k
            # Swap rows in U and P; swap prior parts of L
            if pivot != k:
                U[[k, pivot], :] = U[[pivot, k], :]
                P[[k, pivot], :] = P[[pivot, k], :]
                if k > 0:
                    L[[k, pivot], :k] = L[[pivot, k], :k]

            # Eliminate entries below the pivot
            pivot_val = U[k, k]
            if abs(pivot_val) <= self.tol:
                # Column is effectively zero below and including pivot; skip
                continue

            for i in range(k + 1, n):
                L[i, k] = U[i, k] / pivot_val
                U[i, k:] -= L[i, k] * U[k, k:]
                U[i, k] = 0.0

        return L, U, P

    def solve(self, problem):
        '''
        Solve the lu_factorization problem.
        Args:
            problem: Dictionary containing problem data specific to lu_factorization
        Returns:
            The solution in the format expected by the task
        '''
        A = self._get_matrix_from_problem(problem)
        L, U, P = self._lu_factorization_partial_pivot(A)
        return {
            'L': L.tolist(),
            'U': U.tolist(),
            'P': P.tolist()
        }

    def _as_array(self, x):
        arr = np.array(x, dtype=float)
        return arr

    def _is_permutation_matrix(self, P):
        if P.ndim != 2 or P.shape[0] != P.shape[1]:
            return False
        n = P.shape[0]
        row_sums = np.sum(np.isclose(P, 1.0, atol=self.tol), axis=1) + \
            np.sum(np.isclose(P, 0.0, atol=self.tol), axis=1)
        col_sums = np.sum(np.isclose(P, 1.0, atol=self.tol), axis=0) + \
            np.sum(np.isclose(P, 0.0, atol=self.tol), axis=0)
        # Check that each row/col contains exactly one '1' and the rest '0'
        return (np.all(np.isclose(P @ np.ones((n, 1)), 1.0, atol=self.tol)) and
                np.all(np.isclose(np.ones((1, n)) @ P, 1.0, atol=self.tol)) and
                np.all((P == 0) | (P == 1)))

    def _perm_matrix_from_vector(self, perm):
        perm = np.array(perm, dtype=int)
        n = perm.size
        if sorted(perm.tolist()) != list(range(n)):
            raise ValueError('Invalid permutation vector')
        P = np.zeros((n, n), dtype=float)
        for i, j in enumerate(perm):
            P[i, j] = 1.0
        return P

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        try:
            A = self._get_matrix_from_problem(problem)
            n = A.shape[0]

            # Extract L, U, P in flexible ways
            if 'L' not in solution or 'U' not in solution:
                return False

            L = self._as_array(solution['L'])
            U = self._as_array(solution['U'])

            if L.shape != (n, n) or U.shape != (n, n):
                return False

            # Build/parse P
            P = None
            if 'P' in solution:
                P = self._as_array(solution['P'])
                if P.ndim == 1 and P.size == n:
                    P = self._perm_matrix_from_vector(P)
                elif P.shape != (n, n):
                    return False
            elif 'perm' in solution:
                P = self._perm_matrix_from_vector(solution['perm'])
            elif 'piv' in solution:
                P = self._perm_matrix_from_vector(solution['piv'])
            else:
                # If no permutation given, assume identity
                P = np.eye(n, dtype=float)

            if P.shape != (n, n):
                return False

            # Check triangular properties and unit diagonal on L
            if not np.allclose(np.diag(L), 1.0, atol=self.tol):
                return False
            # L lower-triangular
            if not np.allclose(np.triu(L, k=1), 0.0, atol=self.tol):
                return False
            # U upper-triangular
            if not np.allclose(np.tril(U, k=-1), 0.0, atol=self.tol):
                return False

            # Check decomposition: P A = L U
            left = P @ A
            right = L @ U
            scale = max(1.0, np.linalg.norm(left, ord=np.inf),
                        np.linalg.norm(right, ord=np.inf))
            return np.allclose(left, right, atol=self.tol * scale)
        except Exception:
            return False
