class FFTConvolution:

    def __init__(self):
        pass

    def _next_pow_two(self, n):
        p = 1
        while p < n:
            p <<= 1
        return p

    def _fft(self, a, invert=False):
        n = len(a)
        j = 0
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                a[i], a[j] = a[j], a[i]

        length = 2
        import math
        while length <= n:
            ang = 2 * math.pi / length * (-1 if invert else 1)
            wlen = complex(math.cos(ang), math.sin(ang))
            for i in range(0, n, length):
                w = 1 + 0j
                half = length // 2
                for j in range(i, i + half):
                    u = a[j]
                    v = a[j + half] * w
                    a[j] = u + v
                    a[j + half] = u - v
                    w *= wlen
            length <<= 1

        if invert:
            inv_n = 1.0 / n
            for i in range(n):
                a[i] *= inv_n

    def _convolve(self, a, b, force_int=None):
        if len(a) == 0 or len(b) == 0:
            return []

        n_res = len(a) + len(b) - 1
        n = self._next_pow_two(n_res)

        fa = [0j] * n
        fb = [0j] * n

        a_is_int = all(isinstance(x, (int, bool)) for x in a)
        b_is_int = all(isinstance(x, (int, bool)) for x in b)

        for i in range(len(a)):
            fa[i] = complex(float(a[i]), 0.0)
        for i in range(len(b)):
            fb[i] = complex(float(b[i]), 0.0)

        self._fft(fa, invert=False)
        self._fft(fb, invert=False)

        for i in range(n):
            fa[i] *= fb[i]

        self._fft(fa, invert=True)

        res = [fa[i].real for i in range(n_res)]

        make_int = False
        if force_int is not None:
            make_int = bool(force_int)
        else:
            make_int = a_is_int and b_is_int

        if make_int:
            # Round to nearest int safely
            return [int(round(x)) for x in res]
        return res

    def solve(self, problem):
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
        Returns:
            The solution in the format expected by the task
        '''
        a = problem.get("a", [])
        b = problem.get("b", [])
        force_int = problem.get("as_int", None)
        result = self._convolve(a, b, force_int=force_int)
        # Optional rounding for float outputs
        if not (all(isinstance(x, int) for x in result)):
            decimals = problem.get("decimals", None)
            if isinstance(decimals, int) and decimals >= 0:
                result = [round(x, decimals) for x in result]
        return result

    def is_solution(self, problem, solution):
        a = problem.get("a", [])
        b = problem.get("b", [])
        force_int = problem.get("as_int", None)
        expected = self._convolve(a, b, force_int=force_int)

        if isinstance(solution, dict) and "result" in solution:
            sol = solution["result"]
        else:
            sol = solution

        if not isinstance(sol, (list, tuple)) or len(sol) != len(expected):
            return False

        # Determine tolerance
        tol = problem.get("tolerance", 1e-6)

        if all(isinstance(x, int) for x in expected):
            try:
                return all(int(x) == int(y) for x, y in zip(expected, sol))
            except Exception:
                return False
        else:
            try:
                for x, y in zip(expected, sol):
                    if abs(float(x) - float(y)) > tol:
                        return False
                return True
            except Exception:
                return False
