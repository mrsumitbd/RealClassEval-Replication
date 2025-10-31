class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the Convolve2DFullFill.'''
        pass

    def _extract_matrix(self, problem, keys):
        for k in keys:
            if k in problem and problem[k] is not None:
                return problem[k]
        raise ValueError(
            f"Missing required matrix in problem. Expected one of: {keys}")

    def _to_matrix(self, data, name):
        if isinstance(data, (list, tuple)):
            if len(data) == 0:
                return []
            # Allow 1D array (treat as single row)
            if all(not isinstance(r, (list, tuple)) for r in data):
                return [list(data)]
            # Ensure rectangular 2D list
            rows = [list(r) for r in data]
            max_len = max(len(r) for r in rows) if rows else 0
            for idx, r in enumerate(rows):
                if len(r) != max_len:
                    raise ValueError(
                        f"{name} must be a rectangular 2D array. Row {idx} has length {len(r)} != {max_len}")
            return rows
        else:
            raise TypeError(
                f"{name} must be a list or tuple representing a 2D array")

    def _convolve2d_full(self, A, K):
        # A and K are list of lists (rectangular)
        if A == [] or K == []:
            return []
        hA = len(A)
        wA = len(A[0]) if hA > 0 else 0
        hK = len(K)
        wK = len(K[0]) if hK > 0 else 0

        if hA == 0 or wA == 0 or hK == 0 or wK == 0:
            return []

        H = hA + hK - 1
        W = wA + wK - 1

        # Determine if we should keep integer arithmetic
        def is_int_matrix(M):
            for row in M:
                for v in row:
                    if not isinstance(v, int) and not (isinstance(v, float) and v.is_integer()):
                        return False
            return True

        keep_int = is_int_matrix(A) and is_int_matrix(K)

        out = [[0 for _ in range(W)] for _ in range(H)]
        for oy in range(H):
            for ox in range(W):
                s = 0
                for ky in range(hK):
                    ay = oy - ky
                    if ay < 0 or ay >= hA:
                        continue
                    rowA = A[ay]
                    rowK = K[ky]
                    for kx in range(wK):
                        ax = ox - kx
                        if ax < 0 or ax >= wA:
                            continue
                        s += rowA[ax] * rowK[kx]
                out[oy][ox] = int(s) if keep_int else s
        return out

    def solve(self, problem):
        '''
        Solve the convolve2d_full_fill problem.
        Args:
            problem: Dictionary containing problem data specific to convolve2d_full_fill
        Returns:
            The solution in the format expected by the task
        '''
        A_raw = self._extract_matrix(
            problem, ['input', 'image', 'matrix', 'grid', 'a', 'x', 'arr'])
        K_raw = self._extract_matrix(
            problem, ['kernel', 'filter', 'weights', 'k', 'w'])
        A = self._to_matrix(A_raw, "input")
        K = self._to_matrix(K_raw, "kernel")

        mode = problem.get('mode', 'full')
        if mode not in ('full', None):
            # This solver only supports 'full'
            raise ValueError(
                f"Unsupported mode: {mode}. Only 'full' is supported.")

        result = self._convolve2d_full(A, K)

        # Determine expected output format. Default to raw matrix.
        output_format = problem.get('output_format', 'matrix')
        if output_format == 'matrix':
            return result
        elif output_format == 'flat':
            return [v for row in result for v in row]
        else:
            # Unknown format: return matrix
            return result

    def _almost_equal(self, a, b, tol=1e-9):
        try:
            return abs(a - b) <= tol
        except Exception:
            return a == b

    def _matrices_equal(self, M1, M2, tol=1e-9):
        if isinstance(M1, (list, tuple)) and isinstance(M2, (list, tuple)):
            # If both are 2D matrices
            if len(M1) == 0 and len(M2) == 0:
                return True
            # Try 2D
            if all(isinstance(r, (list, tuple)) for r in M1) and all(isinstance(r, (list, tuple)) for r in M2):
                if len(M1) != len(M2):
                    return False
                for r1, r2 in zip(M1, M2):
                    if len(r1) != len(r2):
                        return False
                    for v1, v2 in zip(r1, r2):
                        if not self._almost_equal(v1, v2, tol):
                            return False
                return True
            # Else treat as flat
            if len(M1) != len(M2):
                return False
            for v1, v2 in zip(M1, M2):
                if not self._almost_equal(v1, v2, tol):
                    return False
            return True
        return self._almost_equal(M1, M2, tol)

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # If expected answer is provided in the problem, compare against it
        expected = None
        for key in ('output', 'expected', 'target', 'result'):
            if key in problem:
                expected = problem[key]
                break

        if expected is not None:
            return self._matrices_equal(solution, expected)

        # Otherwise, recompute using solve and compare
        try:
            computed = self.solve(problem)
        except Exception:
            return False
        return self._matrices_equal(solution, computed)
