class FFTConvolution:

    def __init__(self):
        pass

    def _next_pow_two(self, n):
        if n <= 0:
            return 1
        p = 1
        while p < n:
            p <<= 1
        return p

    def _fft(self, a, invert=False):
        import math
        n = len(a)
        j = 0
        # Bit-reversal permutation
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                a[i], a[j] = a[j], a[i]
        length = 2
        while length <= n:
            ang = (2.0 * math.pi / length) * (1.0 if not invert else -1.0)
            wlen = complex(math.cos(ang), math.sin(ang))
            i = 0
            while i < n:
                w = 1+0j
                half = length >> 1
                for k in range(i, i + half):
                    u = a[k]
                    v = a[k + half] * w
                    a[k] = u + v
                    a[k + half] = u - v
                    w *= wlen
                i += length
            length <<= 1
        if invert:
            inv_n = 1.0 / n
            for i in range(n):
                a[i] *= inv_n
        return a

    def _convolution(self, a, b):
        la, lb = len(a), len(b)
        if la == 0 or lb == 0:
            return []
        n = self._next_pow_two(la + lb - 1)
        fa = [0j] * n
        fb = [0j] * n

        for i, v in enumerate(a):
            fa[i] = complex(v, 0.0)
        for i, v in enumerate(b):
            fb[i] = complex(v, 0.0)

        self._fft(fa, invert=False)
        self._fft(fb, invert=False)
        for i in range(n):
            fa[i] *= fb[i]
        self._fft(fa, invert=True)

        res = [fa[i].real for i in range(la + lb - 1)]
        return res

    def _is_all_ints(self, seq):
        # Treat bool as not int for this context
        return all(isinstance(x, int) and not isinstance(x, bool) for x in seq)

    def _parse_problem(self, problem):
        # Accept various shapes: dict with common keys or tuple/list of length 2
        if isinstance(problem, dict):
            for ka, kb in [
                ("a", "b"),
                ("x", "h"),
                ("lhs", "rhs"),
                ("signal", "kernel"),
                ("u", "v"),
            ]:
                if ka in problem and kb in problem:
                    return problem[ka], problem[kb]
            # Fallback: first two iterable values
            vals = list(problem.values())
            if len(vals) >= 2:
                return vals[0], vals[1]
            raise ValueError("Problem dict must contain two sequences.")
        elif isinstance(problem, (list, tuple)) and len(problem) == 2:
            return problem[0], problem[1]
        else:
            raise ValueError(
                "Problem must be a dict with two sequences or a 2-tuple/list.")

    def solve(self, problem):
        a, b = self._parse_problem(problem)
        a_list = list(a)
        b_list = list(b)

        conv = self._convolution(a_list, b_list)

        # If both inputs are integers, round result to nearest int
        if self._is_all_ints(a_list) and self._is_all_ints(b_list):
            out = []
            for v in conv:
                # clamp tiny numerical noise
                if abs(v) < 1e-9:
                    out.append(0)
                else:
                    out.append(int(round(v)))
            return out
        else:
            # Return floats with minimal noise trimming
            return [0.0 if abs(v) < 1e-12 else v for v in conv]

    def is_solution(self, problem, solution):
        try:
            a, b = self._parse_problem(problem)
            a_list = list(a)
            b_list = list(b)
            # Normalize provided solution to list
            sol = list(solution)

            # Compute reference via naive convolution
            la, lb = len(a_list), len(b_list)
            if la == 0 or lb == 0:
                return sol == []
            ref = [0] * (la + lb - 1)
            for i in range(la):
                ai = a_list[i]
                for j in range(lb):
                    ref[i + j] = ref[i + j] + ai * b_list[j]

            # If integer inputs, cast reference to ints
            if self._is_all_ints(a_list) and self._is_all_ints(b_list):
                ref = [int(v) for v in ref]
                if len(ref) != len(sol):
                    return False
                try:
                    sol_int = [int(x) for x in sol]
                except Exception:
                    return False
                return ref == sol_int
            else:
                # Float comparison with tolerance
                if len(ref) != len(sol):
                    return False
                tol = 1e-6
                for r, s in zip(ref, sol):
                    try:
                        if abs(float(r) - float(s)) > tol:
                            return False
                    except Exception:
                        return False
                return True
        except Exception:
            return False
