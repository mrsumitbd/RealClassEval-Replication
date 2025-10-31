class AffineTransform2D:

    def __init__(self):
        pass

    def solve(self, problem):
        # problem: dict with keys:
        # - 'points_src': list of (x, y)
        # - 'points_dst': list of (u, v)
        # - optional 'tolerance': float
        # Returns dict with keys:
        # - 'matrix': [[a, b, c], [d, e, f]]
        # - 'rms_error': float
        src = problem.get('points_src')
        dst = problem.get('points_dst')
        if not isinstance(src, (list, tuple)) or not isinstance(dst, (list, tuple)):
            raise ValueError(
                "problem must contain 'points_src' and 'points_dst' as lists")
        if len(src) != len(dst):
            raise ValueError(
                "points_src and points_dst must have the same length")
        n = len(src)
        if n < 3:
            raise ValueError(
                "At least 3 point pairs are required to determine an affine transform")

        # Build design matrix M (2n x 6) and RHS y (2n)
        # For each i:
        # [ x y 1 0 0 0 ] [a b c d e f]^T = u
        # [ 0 0 0 x y 1 ] [a b c d e f]^T = v
        M = [[0.0]*6 for _ in range(2*n)]
        y = [0.0]*(2*n)
        for i, ((x, y0), (u, v)) in enumerate(zip(src, dst)):
            row_u = 2*i
            row_v = 2*i + 1
            M[row_u][0] = x
            M[row_u][1] = y0
            M[row_u][2] = 1.0
            M[row_u][3] = 0.0
            M[row_u][4] = 0.0
            M[row_u][5] = 0.0
            y[row_u] = u

            M[row_v][0] = 0.0
            M[row_v][1] = 0.0
            M[row_v][2] = 0.0
            M[row_v][3] = x
            M[row_v][4] = y0
            M[row_v][5] = 1.0
            y[row_v] = v

        # Solve least squares: p = (M^T M)^{-1} M^T y
        Mt = self._transpose(M)
        MtM = self._matmul(Mt, M)  # 6x6
        Mty = self._matvec(Mt, y)  # 6
        p = self._solve_linear_system(MtM, Mty)  # [a,b,c,d,e,f]

        a, b, c, d, e, f = p
        matrix = [[a, b, c],
                  [d, e, f]]

        # Compute RMS error
        se = 0.0
        for (x, y0), (u, v) in zip(src, dst):
            u_hat = a*x + b*y0 + c
            v_hat = d*x + e*y0 + f
            du = u_hat - u
            dv = v_hat - v
            se += du*du + dv*dv
        rms = (se / max(1, n)) ** 0.5

        return {'matrix': matrix, 'rms_error': rms}

    def is_solution(self, problem, solution):
        # Checks if solution maps points within tolerance.
        # problem keys:
        # - 'points_src', 'points_dst'
        # - optional 'tolerance' (default 1e-6)
        # solution keys:
        # - 'matrix': [[a,b,c],[d,e,f]]
        tol = problem.get('tolerance', 1e-6)
        src = problem.get('points_src')
        dst = problem.get('points_dst')
        if not isinstance(solution, dict):
            return False
        mat = solution.get('matrix')
        if (not isinstance(mat, (list, tuple)) or len(mat) != 2 or
                any(not isinstance(row, (list, tuple)) or len(row) != 3 for row in mat)):
            return False
        a, b, c = mat[0]
        d, e, f = mat[1]
        if not isinstance(src, (list, tuple)) or not isinstance(dst, (list, tuple)):
            return False
        if len(src) != len(dst) or len(src) == 0:
            return False

        for (x, y0), (u, v) in zip(src, dst):
            u_hat = a*x + b*y0 + c
            v_hat = d*x + e*y0 + f
            if abs(u_hat - u) > tol or abs(v_hat - v) > tol:
                return False
        return True

    # Linear algebra helpers (pure Python)
    def _transpose(self, A):
        return [list(row) for row in zip(*A)]

    def _matmul(self, A, B):
        # A: m x k, B: k x n -> m x n
        m = len(A)
        k = len(A[0]) if m else 0
        if not B or len(B) != k:
            # Try to handle degenerate inputs
            raise ValueError(
                "Incompatible matrix dimensions for multiplication")
        n = len(B[0]) if k else 0
        C = [[0.0]*n for _ in range(m)]
        # Pretranspose B for cache-friendly access
        Bt = self._transpose(B)
        for i in range(m):
            Ai = A[i]
            for j in range(n):
                s = 0.0
                Bj = Bt[j]
                for t in range(k):
                    s += Ai[t] * Bj[t]
                C[i][j] = s
        return C

    def _matvec(self, A, x):
        # A: m x n, x: n -> m
        m = len(A)
        n = len(A[0]) if m else 0
        if len(x) != n:
            raise ValueError(
                "Incompatible dimensions for matrix-vector multiplication")
        y = [0.0]*m
        for i in range(m):
            s = 0.0
            Ai = A[i]
            for j in range(n):
                s += Ai[j] * x[j]
            y[i] = s
        return y

    def _solve_linear_system(self, A, b):
        # Solve A x = b for square A using Gaussian elimination with partial pivoting
        n = len(A)
        if any(len(row) != n for row in A) or len(b) != n:
            raise ValueError("A must be square and compatible with b")
        # Create augmented matrix
        aug = [list(A[i]) + [b[i]] for i in range(n)]

        for col in range(n):
            # Pivot
            pivot_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
            if abs(aug[pivot_row][col]) < 1e-12:
                raise ValueError("Singular or ill-conditioned system")
            if pivot_row != col:
                aug[col], aug[pivot_row] = aug[pivot_row], aug[col]
            # Normalize pivot row
            pivot = aug[col][col]
            inv_pivot = 1.0 / pivot
            for j in range(col, n+1):
                aug[col][j] *= inv_pivot
            # Eliminate
            for r in range(n):
                if r == col:
                    continue
                factor = aug[r][col]
                if factor == 0.0:
                    continue
                for j in range(col, n+1):
                    aug[r][j] -= factor * aug[col][j]

        # Extract solution
        x = [aug[i][n] for i in range(n)]
        return x
