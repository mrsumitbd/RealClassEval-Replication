class FFTConvolution:

    def __init__(self):
        pass

    def _is_sequence(self, x):
        if isinstance(x, (str, bytes)):
            return False
        try:
            iter(x)
            return True
        except TypeError:
            return False

    def _extract_sequences(self, problem):
        if isinstance(problem, dict):
            for keys in (('a', 'b'), ('x', 'y'), ('u', 'v'), ('seq1', 'seq2')):
                if keys[0] in problem and keys[1] in problem:
                    return list(problem[keys[0]]), list(problem[keys[1]])
            # fallback: take first two iterable values
            vals = [v for v in problem.values() if self._is_sequence(v)]
            if len(vals) >= 2:
                return list(vals[0]), list(vals[1])
            raise ValueError("Problem dict must contain two sequences.")
        if isinstance(problem, (list, tuple)) and len(problem) == 2 and self._is_sequence(problem[0]) and self._is_sequence(problem[1]):
            return list(problem[0]), list(problem[1])
        raise ValueError(
            "Problem must be a dict with two sequences or a tuple/list of two sequences.")

    def _is_all_int(self, seq):
        return all(isinstance(v, (int, bool)) or (isinstance(v, float) and float(v).is_integer()) for v in seq)

    def _next_power_of_two(self, n):
        if n <= 1:
            return 1
        return 1 << (n - 1).bit_length()

    def _fft(self, a, invert=False):
        n = len(a)
        if n == 1:
            return a[:]
        even = self._fft(a[0::2], invert)
        odd = self._fft(a[1::2], invert)
        ang = (-2.0 if invert else 2.0) * 3.141592653589793 / n
        w = complex(1.0, 0.0)
        wn = complex(__import__("math").cos(ang), __import__("math").sin(ang))
        y = [0j] * n
        half = n // 2
        for k in range(half):
            t = w * odd[k]
            y[k] = even[k] + t
            y[k + half] = even[k] - t
            w *= wn
        return y

    def _convolve_fft(self, a, b):
        n = len(a)
        m = len(b)
        if n == 0 or m == 0:
            return []
        size = n + m - 1
        fft_n = self._next_power_of_two(size)
        fa = [complex(x, 0.0) for x in a] + [0j] * (fft_n - n)
        fb = [complex(x, 0.0) for x in b] + [0j] * (fft_n - m)
        fa = self._fft(fa, invert=False)
        fb = self._fft(fb, invert=False)
        for i in range(fft_n):
            fa[i] *= fb[i]
        res_c = self._fft(fa, invert=True)
        inv_n = 1.0 / fft_n
        res = [(res_c[i].real * inv_n) for i in range(size)]
        return res

    def solve(self, problem):
        a, b = self._extract_sequences(problem)
        ints = self._is_all_int(a) and self._is_all_int(b)
        a = [float(x) for x in a]
        b = [float(x) for x in b]
        res = self._convolve_fft(a, b)
        if ints:
            out = [int(round(x)) for x in res]
            return out
        return res

    def is_solution(self, problem, solution):
        try:
            a, b = self._extract_sequences(problem)
        except Exception:
            return False
        # Validate solution is sequence of appropriate length
        if not self._is_sequence(solution):
            return False
        sol = list(solution)
        expected_len = (0 if len(a) == 0 or len(b) ==
                        0 else len(a) + len(b) - 1)
        if len(sol) != expected_len:
            return False
        # Compute direct convolution for verification
        n, m = len(a), len(b)
        if n == 0 or m == 0:
            return len(sol) == 0
        # Promote to float for comparison
        aa = [float(x) for x in a]
        bb = [float(x) for x in b]
        direct = [0.0] * (n + m - 1)
        for i in range(n):
            ai = aa[i]
            for j in range(m):
                direct[i + j] += ai * bb[j]
        # Compare with tolerance
        tol = 1e-6
        if self._is_all_int(a) and self._is_all_int(b):
            # allow integer or near-integer floats
            for s, d in zip(sol, direct):
                try:
                    sv = float(s)
                except Exception:
                    return False
                if abs(sv - round(d)) > 0.5 + tol:
                    return False
            return True
        else:
            for s, d in zip(sol, direct):
                try:
                    sv = float(s)
                except Exception:
                    return False
                if abs(sv - d) > 1e-4 * max(1.0, abs(d)) + tol:
                    return False
            return True
