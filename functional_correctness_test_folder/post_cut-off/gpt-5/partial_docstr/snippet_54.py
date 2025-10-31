class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the Convolve2DFullFill.'''
        pass

    def _shape(self, mat):
        if not isinstance(mat, list) or len(mat) == 0:
            return (0, 0)
        if not isinstance(mat[0], list):
            # treat as 1D row
            return (1, len(mat))
        return (len(mat), len(mat[0]) if len(mat) > 0 else 0)

    def _is_rectangular(self, mat):
        if not isinstance(mat, list):
            return False
        if len(mat) == 0:
            return True
        if not all(isinstance(row, list) for row in mat):
            return False
        row_len = len(mat[0])
        return all(len(row) == row_len for row in mat)

    def _flip_2d(self, mat):
        # Flip both vertically and horizontally
        return [list(reversed(row)) for row in reversed(mat)]

    def _convolve2d_full(self, A, B):
        n1, m1 = self._shape(A)
        n2, m2 = self._shape(B)
        if n1 == 0 or m1 == 0 or n2 == 0 or m2 == 0:
            return []

        # Ensure rectangular
        if not (self._is_rectangular(A) and self._is_rectangular(B)):
            raise ValueError("Inputs must be rectangular 2D lists")

        # Flip kernel for convolution
        K = self._flip_2d(B)

        out_rows = n1 + n2 - 1
        out_cols = m1 + m2 - 1
        out = [[0 for _ in range(out_cols)] for _ in range(out_rows)]

        for i in range(n1):
            Ai = A[i]
            for j in range(m1):
                aij = Ai[j]
                if aij == 0:
                    continue
                # accumulate
                for k in range(n2):
                    Kk = K[k]
                    oi = i + k
                    row_out = out[oi]
                    for l in range(m2):
                        row_out[j + l] += aij * Kk[l]
        return out

    def solve(self, problem):
        # Expect problem as a tuple/list of two 2D lists: (A, B)
        if (not isinstance(problem, (list, tuple))) or len(problem) != 2:
            raise ValueError("Problem must be a pair (A, B) of 2D lists")
        A, B = problem
        return self._convolve2d_full(A, B)

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
            expected = self.solve(problem)
        except Exception:
            return False

        # Simple exact match for ints; allow small tolerance for floats
        def close(a, b, tol=1e-9):
            try:
                return abs(a - b) <= tol
            except Exception:
                return False

        if not isinstance(solution, list):
            return False
        if len(solution) != len(expected):
            return False
        for row_sol, row_exp in zip(solution, expected):
            if not isinstance(row_sol, list) or len(row_sol) != len(row_exp):
                return False
            for x, y in zip(row_sol, row_exp):
                if isinstance(x, float) or isinstance(y, float):
                    if not close(x, y):
                        return False
                else:
                    if x != y:
                        return False
        return True
