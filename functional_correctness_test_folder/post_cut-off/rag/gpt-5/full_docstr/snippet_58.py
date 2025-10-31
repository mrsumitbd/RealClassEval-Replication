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
        A = self._get_matrix(problem)
        A = np.array(A, dtype=float, copy=True)
        if A.ndim != 2:
            raise ValueError('Input matrix A must be 2-dimensional')
        m, n = A.shape
        r = min(m, n)
        tol = float(problem.get('tol', 0.0))

        p = np.arange(m)
        rank = 0

        for k in range(r):
            pivot_row_rel = np.argmax(np.abs(A[k:, k]))
            pivot_row = k + pivot_row_rel
            pivot_val = A[pivot_row, k]

            if abs(pivot_val) <= tol:
                continue

            if pivot_row != k:
                A[[k, pivot_row], :] = A[[pivot_row, k], :]
                p[[k, pivot_row]] = p[[pivot_row, k]]

            rank += 1

            if k + 1 < m:
                A[k + 1:, k] = A[k + 1:, k] / A[k, k]
                if k + 1 < n:
                    A[k + 1:, k + 1:] -= np.outer(A[k + 1:, k], A[k, k + 1:])

        L = np.tril(A, k=-1) + np.eye(m, dtype=A.dtype)
        U = np.triu(A)
        P = np.eye(m)[p]

        solution = {
            'L': L.tolist(),
            'U': U.tolist(),
            'P': P.tolist(),
            'perm': p.tolist(),
            'rank': int(rank)
        }
        return solution

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
            A = self._get_matrix(problem)
            A = np.array(A, dtype=float, copy=False)
            if A.ndim != 2:
                return False
            m, n = A.shape

            if not isinstance(solution, dict):
                return False

            if 'L' not in solution or 'U' not in solution:
                return False

            L = np.array(solution['L'], dtype=float, copy=False)
            U = np.array(solution['U'], dtype=float, copy=False)

            if L.ndim != 2 or U.ndim != 2:
                return False
            if L.shape[0] != m:
                return False
            if L.shape[1] != L.shape[0]:
                # Require square L for a standard LU with partial pivoting
                return False
            if U.shape[0] != L.shape[1] or U.shape[1] != n:
                # U must be compatible with L @ U to yield (m, n)
                return False

            tol = float(problem.get('tol', 1e-8))

            if 'P' in solution:
                P = np.array(solution['P'], dtype=float, copy=False)
                if P.shape != (m, m):
                    return False
                if not self._is_permutation_matrix(P, tol):
                    return False
                left = P @ A
            elif 'perm' in solution:
                perm = np.array(solution['perm'], dtype=int, copy=False)
                if perm.shape != (m,):
                    return False
                if not self._is_valid_permutation_vector(perm, m):
                    return False
                left = A[perm, :]
            else:
                P = np.eye(m)
                left = P @ A

            right = L @ U

            if not np.allclose(left, right, atol=tol, rtol=0):
                return False

            if not self._is_unit_lower_triangular(L, tol):
                return False

            if not self._is_upper_triangular(U, tol):
                return False

            return True
        except Exception:
            return False

    def _get_matrix(self, problem):
        if not isinstance(problem, dict):
            raise ValueError('Problem must be a dictionary')
        if 'A' in problem:
            return problem['A']
        if 'matrix' in problem:
            return problem['matrix']
        if 'data' in problem:
            return problem['data']
        raise ValueError(
            'Problem dictionary must contain key "A" (or "matrix"/"data")')

    def _is_unit_lower_triangular(self, L, tol):
        if L.shape[0] != L.shape[1]:
            return False
        if not np.allclose(np.diag(L), 1.0, atol=tol, rtol=0):
            return False
        upper = np.triu(L, k=1)
        return np.all(np.abs(upper) <= tol)

    def _is_upper_triangular(self, U, tol):
        lower = np.tril(U, k=-1)
        return np.all(np.abs(lower) <= tol)

    def _is_permutation_matrix(self, P, tol):
        if P.shape[0] != P.shape[1]:
            return False
        if not np.all((P >= -tol) & (P <= 1 + tol)):
            return False
        row_sums = np.sum(P, axis=1)
        col_sums = np.sum(P, axis=0)
        if not np.allclose(row_sums, 1.0, atol=tol, rtol=0):
            return False
        if not np.allclose(col_sums, 1.0, atol=tol, rtol=0):
            return False
        # Near-binary check
        rounded = np.round(P)
        return np.allclose(P, rounded, atol=tol, rtol=0)

    def _is_valid_permutation_vector(self, perm, m):
        if perm.ndim != 1 or perm.size != m:
            return False
        if np.any(perm < 0) or np.any(perm >= m):
            return False
        return np.array_equal(np.sort(perm), np.arange(m))
