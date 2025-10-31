class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        pass

    def _get_matrix_from_problem(self, problem):
        keys = ['A', 'matrix', 'mat', 'data']
        A = None
        for k in keys:
            if k in problem:
                A = problem[k]
                break
        if A is None:
            raise ValueError(
                'Problem must contain a matrix under one of keys: A, matrix, mat, data')
        return self._as_matrix(A)

    def _as_matrix(self, mat):
        # Convert nested lists/tuples to list of list of floats; validate rectangular
        if hasattr(mat, 'tolist'):
            mat = mat.tolist()
        if not isinstance(mat, (list, tuple)) or not mat:
            raise ValueError('Matrix must be a non-empty 2D list/tuple')
        rows = []
        ncols = None
        for r in mat:
            if not isinstance(r, (list, tuple)) or not r:
                raise ValueError('Matrix must be a non-empty 2D list/tuple')
            row = [float(x) for x in r]
            if ncols is None:
                ncols = len(row)
            elif len(row) != ncols:
                raise ValueError('Matrix must be rectangular')
            rows.append(row)
        return rows

    def _identity(self, n):
        return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    def _deepcopy(self, M):
        return [row[:] for row in M]

    def _matmul(self, A, B):
        m = len(A)
        kA = len(A[0])
        if len(B) == 0:
            raise ValueError('Invalid matrix multiplication: empty B')
        kB = len(B)
        n = len(B[0])
        if kA != kB:
            raise ValueError('Incompatible shapes for multiplication')
        C = [[0.0] * n for _ in range(m)]
        # Simple triple loop
        for i in range(m):
            Ai = A[i]
            for kk in range(kA):
                a = Ai[kk]
                if a == 0.0:
                    continue
                Bk = B[kk]
                for j in range(n):
                    C[i][j] += a * Bk[j]
        return C

    def _max_abs_column_index(self, U, start_row, col):
        m = len(U)
        max_val = -1.0
        max_idx = start_row
        for i in range(start_row, m):
            v = abs(U[i][col])
            if v > max_val:
                max_val = v
                max_idx = i
        return max_idx, max_val

    def _lu_factorize_partial_pivot(self, A):
        # A is m x n
        m = len(A)
        n = len(A[0])
        U = self._deepcopy(A)
        L = self._identity(m)
        P = self._identity(m)

        piv_steps = min(m, n)
        for k in range(piv_steps):
            # Pivot selection
            p, maxv = self._max_abs_column_index(U, k, k)
            # If pivot row different, swap rows in U, P, and the first k columns of L
            if p != k:
                U[k], U[p] = U[p], U[k]
                P[k], P[p] = P[p], P[k]
                # swap L entries for columns < k
                for j in range(k):
                    L[k][j], L[p][j] = L[p][j], L[k][j]

            # If pivot is zero, skip elimination for this column
            pivot = U[k][k] if k < n else 0.0
            if abs(pivot) < 1e-15:
                # No elimination possible; continue to next column
                continue

            # Eliminate below pivot
            for i in range(k + 1, m):
                L[i][k] = U[i][k] / pivot
                # Row update
                factor = L[i][k]
                if factor != 0.0:
                    for j in range(k, n):
                        U[i][j] -= factor * U[k][j]
                    U[i][k] = 0.0  # enforce exact zero for cleanliness
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
        L, U, P = self._lu_factorize_partial_pivot(A)
        return {'L': L, 'U': U, 'P': P}

    def _shape(self, M):
        return (len(M), len(M[0]) if M and isinstance(M[0], (list, tuple)) else 0)

    def _is_permutation_matrix(self, P, tol=1e-9):
        m, n = self._shape(P)
        if m != n:
            return False
        # Each row and column has exactly one 1 and zeros elsewhere
        for i in range(m):
            cnt = 0
            for j in range(n):
                v = P[i][j]
                if abs(v) > tol and abs(v - 1.0) > tol:
                    return False
                if abs(v - 1.0) <= tol:
                    cnt += 1
            if cnt != 1:
                return False
        # Columns
        for j in range(n):
            cnt = 0
            for i in range(m):
                if abs(P[i][j] - 1.0) <= tol:
                    cnt += 1
            if cnt != 1:
                return False
        return True

    def _is_lower_unit_triangular(self, L, tol=1e-9):
        m, n = self._shape(L)
        if m != n:
            return False
        for i in range(m):
            # diagonal ~ 1
            if abs(L[i][i] - 1.0) > 1e-6:
                return False
            # above diagonal ~ 0
            for j in range(i + 1, n):
                if abs(L[i][j]) > tol:
                    return False
        return True

    def _is_upper_triangular(self, U, tol=1e-9):
        m, n = self._shape(U)
        # Allow upper trapezoidal if m != n; enforce zeros below main diagonal
        diag_len = min(m, n)
        for i in range(m):
            for j in range(min(i, n)):
                if j < i and abs(U[i][j]) > tol:
                    return False
        return True

    def _max_abs(self, M):
        return max((abs(x) for row in M for x in row), default=0.0)

    def _mat_diff_max(self, A, B):
        m, n = self._shape(A)
        if self._shape(B) != (m, n):
            raise ValueError('Shape mismatch in matrix difference')
        d = 0.0
        for i in range(m):
            for j in range(n):
                v = abs(A[i][j] - B[i][j])
                if v > d:
                    d = v
        return d

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
        except Exception:
            return False

        if not isinstance(solution, dict):
            return False
        if not all(k in solution for k in ('L', 'U', 'P')):
            return False

        try:
            L = self._as_matrix(solution['L'])
            U = self._as_matrix(solution['U'])
            P = self._as_matrix(solution['P'])
        except Exception:
            return False

        m, n = self._shape(A)
        mL, nL = self._shape(L)
        mU, nU = self._shape(U)
        mP, nP = self._shape(P)

        # Expect shapes: L m x m, U m x n, P m x m
        if not (mL == m and nL == m and mU == m and nU == n and mP == m and nP == m):
            return False

        # Structural checks
        if not self._is_permutation_matrix(P):
            return False
        if not self._is_lower_unit_triangular(L):
            return False
        if not self._is_upper_triangular(U):
            return False

        # Check PA = LU within tolerance
        try:
            PA = self._matmul(P, A)
            LU = self._matmul(L, U)
        except Exception:
            return False

        scale = max(self._max_abs(PA), self._max_abs(LU), 1.0)
        diff = self._mat_diff_max(PA, LU)
        tol = 1e-7 * scale + 1e-12
        return diff <= tol
