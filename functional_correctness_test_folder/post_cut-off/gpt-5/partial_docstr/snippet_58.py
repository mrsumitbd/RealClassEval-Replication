class LUFactorization:

    def __init__(self):
        pass

    def solve(self, problem):
        '''
        Solve the lu_factorization problem.
        Args:
            problem: Dictionary containing problem data specific to lu_factorization.
                     Expected keys:
                       - 'A': square matrix (list of lists of numbers)
                       - 'b': RHS vector (list of numbers) or matrix (list of lists) for multiple RHS
        Returns:
            Solution vector (list of floats) or matrix (list of lists) matching the shape of 'b'.
        '''
        A = problem.get('A', None)
        b = problem.get('b', None)
        if A is None or b is None:
            raise ValueError("Problem must contain 'A' and 'b'.")

        A = self._copy_matrix(A)
        n = len(A)
        if n == 0 or any(len(row) != n for row in A):
            raise ValueError("Matrix 'A' must be non-empty and square.")

        # Normalize b to 2D list: n x m
        b_mat, is_vector = self._normalize_rhs(b, n)

        LU, swaps = self._lu_decompose_with_pivoting(A)

        # Apply the same row swaps to b
        self._apply_swaps_to_rhs(b_mat, swaps)

        # Solve for each RHS column
        X = []
        for j in range(len(b_mat[0])):
            col_b = [b_mat[i][j] for i in range(n)]
            y = self._forward_substitution_unit_lower(LU, col_b)
            x = self._back_substitution_upper(LU, y)
            X.append(x)
        # Reformat to original shape
        if is_vector:
            return [X[0][i] for i in range(n)]
        else:
            # Return n x m matrix
            m = len(X)
            result = [[X[j][i] for j in range(m)] for i in range(n)]
            return result

    def is_solution(self, problem, solution):
        A = problem.get('A', None)
        b = problem.get('b', None)
        if A is None or b is None:
            return False

        n = len(A)
        if n == 0 or any(len(row) != n for row in A):
            return False

        # Normalize b and solution to 2D
        try:
            b_mat, _ = self._normalize_rhs(b, n)
        except Exception:
            return False

        # Normalize solution to 2D with same number of RHS columns
        try:
            sol_mat, is_vector = self._normalize_rhs(solution, n)
        except Exception:
            return False

        if len(b_mat[0]) != len(sol_mat[0]):
            return False

        # Compute A * solution and compare to b
        Ax = self._matmul(A, sol_mat)
        return self._approximately_equal(Ax, b_mat)

    # Helpers

    def _copy_matrix(self, A):
        return [list(map(float, row)) for row in A]

    def _normalize_rhs(self, b, n):
        # Returns (n x m matrix, is_vector)
        # Accept vector (len n) or matrix (n x m)
        if isinstance(b, (list, tuple)) and len(b) > 0 and not isinstance(b[0], (list, tuple)):
            if len(b) != n:
                raise ValueError("RHS vector length must match A dimension.")
            col = [float(v) for v in b]
            return [[col[i]] for i in range(n)], True
        elif isinstance(b, (list, tuple)) and (len(b) == 0 or isinstance(b[0], (list, tuple))):
            # Matrix case
            if len(b) != n:
                raise ValueError(
                    "RHS matrix row count must match A dimension.")
            m = 0 if len(b) == 0 else len(b[0])
            for row in b:
                if len(row) != m:
                    raise ValueError("All RHS rows must have the same length.")
            mat = [[float(val) for val in row] for row in b]
            return mat, False
        else:
            raise ValueError("Unsupported RHS format.")

    def _lu_decompose_with_pivoting(self, A):
        n = len(A)
        swaps = []
        for k in range(n):
            # Partial pivoting: find pivot row
            pivot_row = max(range(k, n), key=lambda i: abs(A[i][k]))
            if abs(A[pivot_row][k]) < 1e-15:
                raise ValueError("Matrix is singular to working precision.")
            if pivot_row != k:
                A[k], A[pivot_row] = A[pivot_row], A[k]
                swaps.append((k, pivot_row))
            # Elimination
            for i in range(k + 1, n):
                A[i][k] /= A[k][k]
                factor = A[i][k]
                # Update the rest of the row
                for j in range(k + 1, n):
                    A[i][j] -= factor * A[k][j]
        return A, swaps

    def _apply_swaps_to_rhs(self, B, swaps):
        # B is n x m
        for k, p in swaps:
            B[k], B[p] = B[p], B[k]

    def _forward_substitution_unit_lower(self, LU, b):
        n = len(LU)
        y = [0.0] * n
        for i in range(n):
            s = b[i]
            for j in range(i):
                s -= LU[i][j] * y[j]
            y[i] = s  # L has unit diagonal
        return y

    def _back_substitution_upper(self, LU, y):
        n = len(LU)
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            s = y[i]
            for j in range(i + 1, n):
                s -= LU[i][j] * x[j]
            denom = LU[i][i]
            if abs(denom) < 1e-15:
                raise ValueError("Matrix is singular to working precision.")
            x[i] = s / denom
        return x

    def _matmul(self, A, X):
        n = len(A)
        m = len(X[0])
        result = [[0.0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for k in range(n):
                aik = A[i][k]
                for j in range(m):
                    result[i][j] += aik * X[k][j]
        return result

    def _approximately_equal(self, M1, M2, rtol=1e-7, atol=1e-9):
        n = len(M1)
        if len(M2) != n or (n > 0 and len(M1[0]) != len(M2[0])):
            return False
        rows = n
        cols = 0 if n == 0 else len(M1[0])
        for i in range(rows):
            for j in range(cols):
                a = M1[i][j]
                b = M2[i][j]
                if not (abs(a - b) <= atol + rtol * max(abs(a), abs(b))):
                    return False
        return True
