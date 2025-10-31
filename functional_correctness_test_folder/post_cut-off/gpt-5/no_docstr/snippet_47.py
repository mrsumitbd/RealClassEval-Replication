class Convolve2DFullFill:

    def __init__(self):
        pass

    def _extract_arrays(self, problem):
        if problem is None:
            raise ValueError("Problem is None")
        if isinstance(problem, dict):
            cand_pairs = [
                ("image", "kernel"),
                ("a", "b"),
                ("A", "B"),
                ("x", "h"),
                ("X", "H"),
                ("mat1", "mat2"),
                ("left", "right"),
            ]
            for k1, k2 in cand_pairs:
                if k1 in problem and k2 in problem:
                    return self._to_2d(problem[k1]), self._to_2d(problem[k2])
            # Fallback if someone used a tuple or list under a key
            for key in ("data", "inputs", "arrays"):
                if key in problem and isinstance(problem[key], (list, tuple)) and len(problem[key]) == 2:
                    a, b = problem[key]
                    return self._to_2d(a), self._to_2d(b)
            raise KeyError("Could not find two 2D arrays in the problem dict")
        elif isinstance(problem, (list, tuple)) and len(problem) == 2:
            return self._to_2d(problem[0]), self._to_2d(problem[1])
        else:
            raise TypeError("Unsupported problem format")

    def _to_2d(self, arr):
        # Convert to list of lists and validate rectangular matrix
        if isinstance(arr, (tuple, list)):
            if len(arr) == 0:
                return []
            if isinstance(arr[0], (list, tuple)):
                rows = [list(r) for r in arr]
                # allow empty rows only if all empty
                if any(len(r) != len(rows[0]) for r in rows):
                    raise ValueError("Non-rectangular 2D array")
                return rows
            else:
                # Treat 1D as a single-row 2D
                return [list(arr)]
        else:
            # Scalar -> 1x1
            return [[arr]]

    def _conv2d_full(self, a, b):
        na = len(a)
        ma = len(a[0]) if na > 0 else 0
        nb = len(b)
        mb = len(b[0]) if nb > 0 else 0

        # Handle empty cases
        if na == 0 or ma == 0 or nb == 0 or mb == 0:
            # By convention, full conv of empty with anything -> empty
            return []

        # Flip kernel
        bf = [[b[nb - 1 - i][mb - 1 - j]
               for j in range(mb)] for i in range(nb)]

        out_n = na + nb - 1
        out_m = ma + mb - 1
        out = [[0 for _ in range(out_m)] for _ in range(out_n)]

        for oi in range(out_n):
            # i in a: 0..na-1
            # ki = oi - i in 0..nb-1 -> i in [oi-(nb-1), oi]
            i_start = max(0, oi - (nb - 1))
            i_end = min(na - 1, oi)
            for oj in range(out_m):
                j_start = max(0, oj - (mb - 1))
                j_end = min(ma - 1, oj)
                s = 0
                for i in range(i_start, i_end + 1):
                    ki = oi - i  # 0..nb-1
                    row_a = a[i]
                    row_bf = bf[ki]
                    for j in range(j_start, j_end + 1):
                        kj = oj - j  # 0..mb-1
                        s += row_a[j] * row_bf[kj]
                out[oi][oj] = s
        return out

    def solve(self, problem):
        a, b = self._extract_arrays(problem)
        return self._conv2d_full(a, b)

    def _extract_solution_array(self, solution):
        if isinstance(solution, (list, tuple)):
            # If 2D numeric list
            if len(solution) == 0:
                return []
            if isinstance(solution[0], (list, tuple)):
                return [list(r) for r in solution]
            else:
                # Treat 1D as 2D single row
                return [list(solution)]
        if isinstance(solution, dict):
            for key in ("result", "out", "y", "C", "conv", "convolution"):
                if key in solution:
                    return self._extract_solution_array(solution[key])
        raise TypeError("Unsupported solution format")

    def is_solution(self, problem, solution):
        try:
            expected = self.solve(problem)
            got = self._extract_solution_array(solution)
        except Exception:
            return False
        # Compare shapes and values with tolerance for floats
        if len(expected) != len(got):
            return False
        if len(expected) == 0:
            return True
        if len(expected[0]) != len(got[0]):
            return False

        def almost_equal(x, y, tol=1e-9):
            try:
                return abs(x - y) <= tol
            except Exception:
                return x == y

        for i in range(len(expected)):
            if len(expected[i]) != len(got[i]):
                return False
            for j in range(len(expected[i])):
                if not almost_equal(expected[i][j], got[i][j]):
                    return False
        return True
