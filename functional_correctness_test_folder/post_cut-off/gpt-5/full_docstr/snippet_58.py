class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        self.tol = 1e-8

    def _to_matrix(self, data):
        if not isinstance(data, (list, tuple)):
            raise ValueError("Matrix must be a list or tuple of rows")
        mat = [list(map(float, row)) for row in data]
        if len(mat) == 0 or any(len(row) != len(mat[0]) for row in mat):
            raise ValueError("Matrix must be non-empty and rectangular")
        return mat

    def _shape(self, A):
        return (len(A), len(A[0]) if A else 0)

    def _identity(self, n):
        return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    def _zeros(self, m, n):
        return [[0.0 for _ in range(n)] for _ in range(m)]

    def _copy(self, A):
        return [row[:] for row in A]

    def _swap_rows(self, A, i, j):
        if i != j:
            A[i], A[j] = A[j], A[i]

    def _matmul(self, A, B):
        m, k1 = self._shape(A)
        k2, n = self._shape(B)
        if k1 != k2:
            raise ValueError("Incompatible shapes for multiplication")
        C = self._zeros(m, n)
        for i in range(m):
            Ai = A[i]
            for t in range(k1):
                a = Ai[t]
                if abs(a) < 1e-300:
                    continue
                Bt = B[t]
                for j in range(n):
                    C[i][j] += a * Bt[j]
        return C

    def _max_abs_diff(self, A, B):
        if self._shape(A) != self._shape(B):
            return float("inf")
        m, n = self._shape(A)
        mad = 0.0
        for i in range(m):
            for j in range(n):
                d = abs(A[i][j] - B[i][j])
                if d > mad:
                    mad = d
        return mad

    def _is_permutation_matrix(self, P):
        m, n = self._shape(P)
        if m != n:
            return False
        used_rows = [False] * m
        used_cols = [False] * n
        for i in range(m):
            ones_in_row = 0
            pos = -1
            for j in range(n):
                v = P[i][j]
                if abs(v - 1.0) < self.tol:
                    ones_in_row += 1
                    pos = j
                elif abs(v) > self.tol:
                    return False
            if ones_in_row != 1:
                return False
            if used_cols[pos]:
                return False
            used_rows[i] = True
            used_cols[pos] = True
        return all(used_rows) and all(used_cols)

    def _is_unit_lower(self, L):
        m, n = self._shape(L)
        if m != n:
            return False
        for i in range(m):
            for j in range(n):
                v = L[i][j]
                if i == j:
                    if abs(v - 1.0) > self.tol:
                        return False
                elif j > i:
                    if abs(v) > self.tol:
                        return False
        return True

    def _is_upper_triangular(self, U):
        m, n = self._shape(U)
        if m != n:
            return False
        for i in range(m):
            for j in range(i):
                if abs(U[i][j]) > self.tol:
                    return False
        return True

    def _build_permutation_from_pivots(self, pivots):
        n = len(pivots)
        P = self._identity(n)
        # Apply swaps to identity in the same order as performed
        for k, p in enumerate(pivots):
            if p != k:
                self._swap_rows(P, k, p)
        return P

    def solve(self, problem):
        '''
        Solve the lu_factorization problem.
        Args:
            problem: Dictionary containing problem data specific to lu_factorization
        Returns:
            The solution in the format expected by the task
        '''
        if not isinstance(problem, dict) or "matrix" not in problem:
            raise ValueError("Problem must be a dict with key 'matrix'")
        A = self._to_matrix(problem["matrix"])
        n, m = self._shape(A)
        if n != m:
            raise ValueError("Only square matrices are supported")
        n = len(A)
        U = self._copy(A)
        L = self._identity(n)
        pivots = list(range(n))
        for k in range(n):
            # Partial pivoting
            pivot_row = k
            max_val = abs(U[k][k])
            for i in range(k + 1, n):
                val = abs(U[i][k])
                if val > max_val:
                    max_val = val
                    pivot_row = i
            if pivot_row != k:
                self._swap_rows(U, k, pivot_row)
                self._swap_rows(pivots, k, pivot_row)
                # Swap corresponding L rows for columns < k
                for j in range(k):
                    L[k][j], L[pivot_row][j] = L[pivot_row][j], L[k][j]
            # Elimination
            pivot = U[k][k]
            if abs(pivot) < self.tol:
                # Singular or nearly singular pivot; skip elimination to avoid blow-up
                continue
            for i in range(k + 1, n):
                L[i][k] = U[i][k] / pivot
                factor = L[i][k]
                if abs(factor) < 1e-300:
                    continue
                for j in range(k, n):
                    U[i][j] -= factor * U[k][j]
        P = self._build_permutation_from_pivots(pivots)
        # Convert to standard python lists (already lists)
        return {"L": L, "U": U, "P": P, "pivots": pivots}

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
            if not isinstance(problem, dict) or "matrix" not in problem:
                return False
            A = self._to_matrix(problem["matrix"])
            n, m = self._shape(A)
            if n != m:
                return False
            if not isinstance(solution, dict):
                return False
            L = self._to_matrix(solution.get("L", []))
            U = self._to_matrix(solution.get("U", []))
            P = self._to_matrix(solution.get("P", []))
            if self._shape(L) != (n, n) or self._shape(U) != (n, n) or self._shape(P) != (n, n):
                return False
            if not self._is_unit_lower(L):
                return False
            if not self._is_upper_triangular(U):
                return False
            if not self._is_permutation_matrix(P):
                return False
            PA = self._matmul(P, A)
            LU = self._matmul(L, U)
            return self._max_abs_diff(PA, LU) <= 1e-6
        except Exception:
            return False
