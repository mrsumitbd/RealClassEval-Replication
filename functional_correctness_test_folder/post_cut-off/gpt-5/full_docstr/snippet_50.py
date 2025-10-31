class FFTConvolution:
    '''
    Initial implementation of fft_convolution task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTConvolution.'''
        pass

    def _next_pow2(self, n):
        p = 1
        while p < n:
            p <<= 1
        return p

    def _fft(self, a, invert=False):
        n = len(a)
        if n == 1:
            return a[:]
        even = self._fft(a[0::2], invert)
        odd = self._fft(a[1::2], invert)
        ang = (-2.0 if invert else 2.0) * 3.141592653589793 / n
        w = 1+0j
        wn = complex(cos := __import__('math').cos(ang),
                     sin := __import__('math').sin(ang))
        # Create combined list
        y = [0j] * n
        for k in range(n // 2):
            t = w * odd[k]
            y[k] = even[k] + t
            y[k + n // 2] = even[k] - t
            w *= wn
        if invert:
            return [val / 2 for val in y]
        return y

    def _fft_iterative(self, a, invert=False):
        # Fallback iterative FFT for performance and to avoid recursion limits
        import math
        n = len(a)
        j = 0
        A = list(a)
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                A[i], A[j] = A[j], A[i]
        length = 2
        while length <= n:
            ang = (-2.0 if invert else 2.0) * math.pi / length
            wlen = complex(math.cos(ang), math.sin(ang))
            for i in range(0, n, length):
                w = 1+0j
                half = length // 2
                for j in range(i, i + half):
                    u = A[j]
                    v = A[j + half] * w
                    A[j] = u + v
                    A[j + half] = u - v
                    w *= wlen
            length <<= 1
        if invert:
            return [x / n for x in A]
        return A

    def _convolve_fft(self, a, b):
        n = len(a)
        m = len(b)
        if n == 0 or m == 0:
            return []
        size = self._next_pow2(n + m - 1)
        fa = [0j] * size
        fb = [0j] * size
        for i, v in enumerate(a):
            fa[i] = complex(v, 0.0)
        for i, v in enumerate(b):
            fb[i] = complex(v, 0.0)
        # Use iterative FFT
        Fa = self._fft_iterative(fa, invert=False)
        Fb = self._fft_iterative(fb, invert=False)
        Fc = [Fa[i] * Fb[i] for i in range(size)]
        c = self._fft_iterative(Fc, invert=True)
        # Trim to full length
        res = c[:n + m - 1]
        return res

    def _as_numeric_list(self, seq):
        # Convert input to list of numbers (int/float), raise for invalid
        out = []
        for x in seq:
            if isinstance(x, (int, float)):
                out.append(float(x))
            elif isinstance(x, complex):
                out.append(float(x.real))
            else:
                # Try to coerce
                try:
                    out.append(float(x))
                except Exception:
                    raise ValueError("Non-numeric element in sequence")
        return out

    def _select_mode(self, full, n, m, mode, first_len_ref):
        # full is list of floats (convolution of length n+m-1)
        if mode == 'full' or mode is None:
            return full
        if mode == 'same':
            L = first_len_ref
            total = n + m - 1
            # center the result to length L
            start = (total - L) // 2
            return full[start:start + L]
        if mode == 'valid':
            if n >= m:
                L = n - m + 1
                start = m - 1
                return full[start:start + L]
            else:
                L = m - n + 1
                start = n - 1
                return full[start:start + L]
        raise ValueError("Invalid mode")

    def _maybe_round_int(self, a_raw, b_raw, values):
        a_is_int = all(isinstance(x, int) or (isinstance(
            x, float) and float(x).is_integer()) for x in a_raw)
        b_is_int = all(isinstance(x, int) or (isinstance(
            x, float) and float(x).is_integer()) for x in b_raw)
        if a_is_int and b_is_int:
            # Round to nearest int
            rounded = []
            for v in values:
                # v could be complex (small imag). Take real part.
                if isinstance(v, complex):
                    v = v.real
                rv = int(round(v))
                rounded.append(rv)
            return rounded
        # Else return real parts as floats
        out = []
        for v in values:
            if isinstance(v, complex):
                out.append(float(v.real))
            else:
                out.append(float(v))
        return out

    def solve(self, problem):
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
        Returns:
            The solution in the format expected by the task
        '''
        if not isinstance(problem, dict):
            raise ValueError("Problem must be a dictionary")
        a = None
        b = None
        if 'a' in problem and 'b' in problem:
            a = problem['a']
            b = problem['b']
        elif 'signal' in problem and 'kernel' in problem:
            a = problem['signal']
            b = problem['kernel']
        else:
            # Try generic keys
            keys = list(problem.keys())
            if len(keys) >= 2:
                a = problem[keys[0]]
                b = problem[keys[1]]
            else:
                raise ValueError("Problem must contain two sequences")
        mode = problem.get('mode', 'full')
        if mode not in ('full', 'same', 'valid'):
            # Accept numpy-like constants if provided
            mode = str(mode).lower()
        a_raw = list(a)
        b_raw = list(b)
        a_num = self._as_numeric_list(a_raw)
        b_num = self._as_numeric_list(b_raw)
        full = self._convolve_fft(a_num, b_num)
        # choose mode; reference length for 'same' is length of first sequence
        selected = self._select_mode(
            full, len(a_num), len(b_num), mode, len(a_num))
        result = self._maybe_round_int(a_raw, b_raw, selected)
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
        try:
            expected = self.solve(problem)
        except Exception:
            return False
        # Normalize solution to list
        if isinstance(solution, (list, tuple)):
            sol_list = list(solution)
        else:
            return False
        if len(sol_list) != len(expected):
            return False
        # Compare with tolerance for floats
        for s, e in zip(sol_list, expected):
            if isinstance(e, int):
                try:
                    if int(s) != e:
                        return False
                except Exception:
                    return False
            else:
                try:
                    sf = float(s)
                except Exception:
                    return False
                if abs(sf - float(e)) > 1e-6:
                    return False
        return True
