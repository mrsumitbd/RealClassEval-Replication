class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        self.tol = 1e-8

    def _to_complex(self, x):
        if isinstance(x, complex):
            return x
        if isinstance(x, (int, float)):
            return complex(x)
        if isinstance(x, (tuple, list)) and len(x) == 2:
            return complex(x[0], x[1])
        if isinstance(x, str):
            return complex(x)
        return complex(x)

    def _normalize_matrix(self, A):
        return [[self._to_complex(v) for v in row] for row in A]

    def _identity(self, n):
        return [[(1+0j) if i == j else (0+0j) for j in range(n)] for i in range(n)]

    def _sub_lambda_I(self, A, lam):
        n = len(A)
        M = [row[:] for row in A]
        for i in range(n):
            M[i][i] -= lam
        return M

    def _rref(self, M):
        # Returns RREF of M and list of pivot columns
        A = [row[:] for row in M]
        m = len(A)
        n = len(A[0]) if m > 0 else 0
        i = 0
        pivots = []
        for j in range(n):
            # Find pivot row
            pivot_row = None
            max_abs = 0.0
            for k in range(i, m):
                val = A[k][j]
                if abs(val) > max_abs + 0.0:
                    max_abs = abs(val)
                    pivot_row = k
            if pivot_row is None or max_abs <= self.tol:
                continue
            # Swap to current row
            if pivot_row != i:
                A[i], A[pivot_row] = A[pivot_row], A[i]
            # Normalize pivot row
            pivot_val = A[i][j]
            A[i] = [x / pivot_val for x in A[i]]
            # Eliminate other rows
            for k in range(m):
                if k == i:
                    continue
                factor = A[k][j]
                if abs(factor) > self.tol:
                    A[k] = [A[k][c] - factor * A[i][c] for c in range(n)]
            pivots.append(j)
            i += 1
            if i == m:
                break
        # Zero out tiny values
        for r in range(m):
            for c in range(n):
                if abs(A[r][c].real) < self.tol:
                    A[r][c] = complex(0.0, A[r][c].imag)
                if abs(A[r][c].imag) < self.tol:
                    A[r][c] = complex(A[r][c].real, 0.0)
                if abs(A[r][c]) < self.tol:
                    A[r][c] = 0.0 + 0.0j
        return A, pivots

    def _nullspace_basis(self, M):
        # Compute a basis for nullspace of M using RREF
        rref, pivots = self._rref(M)
        m = len(rref)
        n = len(rref[0]) if m > 0 else 0
        pivot_set = set(pivots)
        free_cols = [j for j in range(n) if j not in pivot_set]
        basis = []
        if n == 0:
            return basis
        # Map pivot rows to pivot columns
        pivot_rows = []
        row_i = 0
        for j in range(n):
            if row_i < m and j in pivot_set:
                pivot_rows.append(row_i)
                row_i += 1
        # For each free column, construct a vector
        for free in free_cols:
            v = [0.0 + 0.0j for _ in range(n)]
            v[free] = 1.0 + 0.0j
            # For each pivot row r with pivot at col p, set v[p] = - rref[r][free]
            pr_idx = 0
            for p in range(n):
                if p in pivot_set:
                    r = pivot_rows[pr_idx]
                    pr_idx += 1
                    coeff = rref[r][free] if r < m else 0.0 + 0.0j
                    v[p] = -coeff
            basis.append(v)
        # If full rank (no free columns) but rows < n, then zero basis
        return basis

    def _pick_one_vector(self, basis):
        if not basis:
            return None
        # Choose the first basis vector
        v = basis[0][:]
        # Normalize deterministically:
        # - Find index of component with largest magnitude
        # - Scale so that component has magnitude 1 and real part >= 0
        max_idx = None
        max_val = 0.0
        for i, val in enumerate(v):
            a = abs(val)
            if a > max_val:
                max_val = a
                max_idx = i
        if max_idx is None or max_val <= self.tol:
            return None
        pivot_val = v[max_idx]
        scale = 1.0 / pivot_val if abs(pivot_val) > 0 else 1.0 + 0.0j
        v = [x * scale for x in v]
        # Adjust phase to make pivot component real and positive
        pv = v[max_idx]
        if abs(pv) > self.tol:
            phase = pv / abs(pv)
            v = [x / phase for x in v]
        # Zero tiny values
        v = [0.0 + 0.0j if abs(x) < self.tol else x for x in v]
        return v

    def _matvec(self, A, v):
        return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]

    def _norm2(self, v):
        return (sum((abs(x) ** 2) for x in v)) ** 0.5

    def _validate_matrix(self, A):
        if not isinstance(A, (list, tuple)) or not A:
            return False
        n = len(A)
        for row in A:
            if not isinstance(row, (list, tuple)) or len(row) != n:
                return False
        return True

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
        Returns:
            The solution in the format expected by the task
        '''
        if not isinstance(problem, dict):
            return None
        A = problem.get("A") or problem.get("matrix")
        if A is None or not self._validate_matrix(A):
            return None
        A = self._normalize_matrix(A)
        n = len(A)
        if problem.get("lambda") is not None:
            lambdas = [self._to_complex(problem["lambda"])]
            single = True
        elif problem.get("eigenvalue") is not None:
            lambdas = [self._to_complex(problem["eigenvalue"])]
            single = True
        elif problem.get("eigenvalues") is not None:
            lambdas = [self._to_complex(x) for x in problem["eigenvalues"]]
            single = False
        else:
            return None

        result = []
        for lam in lambdas:
            M = self._sub_lambda_I(A, lam)
            basis = self._nullspace_basis(M)
            v = self._pick_one_vector(basis)
            if v is None:
                result.append(None)
            else:
                # Ensure vector length matches n
                if len(v) != n:
                    v = (v + [0.0 + 0.0j] * n)[:n]
                result.append(v)

        if single:
            return result[0]
        return result

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        if not isinstance(problem, dict):
            return False
        A = problem.get("A") or problem.get("matrix")
        if A is None or not self._validate_matrix(A):
            return False
        A = self._normalize_matrix(A)
        n = len(A)

        # Get eigenvalues
        if problem.get("lambda") is not None:
            lambdas = [self._to_complex(problem["lambda"])]
            expect_list = False
        elif problem.get("eigenvalue") is not None:
            lambdas = [self._to_complex(problem["eigenvalue"])]
            expect_list = False
        elif problem.get("eigenvalues") is not None:
            lambdas = [self._to_complex(x) for x in problem["eigenvalues"]]
            expect_list = True
        else:
            return False

        # Normalize solution format
        sols = None
        if expect_list:
            if not isinstance(solution, (list, tuple)) or len(solution) != len(lambdas):
                return False
            sols = solution
        else:
            if isinstance(solution, (list, tuple)) and len(solution) == n and not any(isinstance(x, (list, tuple)) for x in solution):
                sols = [solution]
            elif isinstance(solution, (list, tuple)) and len(solution) == 1 and isinstance(solution[0], (list, tuple)):
                sols = [solution[0]]
            else:
                return False

        for v, lam in zip(sols, lambdas):
            if v is None:
                return False
            if not isinstance(v, (list, tuple)) or len(v) != n:
                return False
            vv = [self._to_complex(x) for x in v]
            # Non-zero vector check
            if self._norm2(vv) <= self.tol:
                return False
            Av = self._matvec(A, vv)
            lv = [lam * x for x in vv]
            res = [Av[i] - lv[i] for i in range(n)]
            res_norm = self._norm2(res)
            v_norm = self._norm2(vv)
            # Relative tolerance check
            if res_norm > 1e-6 * (1.0 + v_norm):
                return False
        return True
