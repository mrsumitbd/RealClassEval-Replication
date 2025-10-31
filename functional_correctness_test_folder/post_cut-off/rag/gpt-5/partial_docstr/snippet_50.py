class FFTConvolution:
    '''
    Initial implementation of fft_convolution task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTConvolution.'''
        try:
            import numpy as _np  # lazy check
            self._np_available = True
        except Exception:
            self._np_available = False

    def solve(self, problem):
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
        Returns:
            The solution in the format expected by the task
        '''
        a, b, cfg = self._extract_problem(problem)
        if a is None or b is None:
            return []

        result = self._convolve(a, b, cfg)

        # Output format selection
        output_format = problem.get(
            'output_format') or problem.get('return') or 'list'
        result_key = problem.get('result_key') or 'result'
        if output_format == 'dict':
            return {result_key: result}
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
        a, b, cfg = self._extract_problem(problem)
        if a is None or b is None:
            # If problem cannot be interpreted, only accept empty solution
            return solution == [] or solution == {} or solution is None

        expected = self._convolve(a, b, cfg)

        # Extract candidate result from solution
        candidate = None
        if isinstance(solution, (list, tuple)):
            candidate = list(solution)
        elif isinstance(solution, dict):
            for key in ('result', 'convolution', 'y', 'output', 'values'):
                if key in solution and isinstance(solution[key], (list, tuple)):
                    candidate = list(solution[key])
                    break

        if candidate is None:
            return False

        if len(candidate) != len(expected):
            return False

        # Compare with tolerance
        atol = float(problem.get('atol', 1e-8))
        rtol = float(problem.get('rtol', 1e-8))
        mod = problem.get('mod', None)

        # If modular comparison requested
        if mod is not None:
            try:
                m = int(mod)
            except Exception:
                m = None
            if m and m > 0:
                try:
                    cand_mod = [int(round(x)) % m for x in candidate]
                    exp_mod = [int(round(x)) % m for x in expected]
                    return cand_mod == exp_mod
                except Exception:
                    return False

        # Otherwise numeric compare
        all_ints = self._all_ints(a) and self._all_ints(b)
        for x, y in zip(candidate, expected):
            if all_ints:
                # integer inputs -> strict integer outputs by default
                try:
                    if int(round(x)) != int(round(y)):
                        return False
                except Exception:
                    return False
            else:
                # float compare
                try:
                    diff = abs(float(x) - float(y))
                    tol = atol + rtol * max(abs(float(x)), abs(float(y)))
                    if diff > tol:
                        return False
                except Exception:
                    return False
        return True

    # --------------------- Internal utilities ---------------------

    def _extract_problem(self, problem):
        # Try to extract two sequences and configuration
        if not isinstance(problem, dict):
            return None, None, {}

        # Direct arrays key
        a = b = None
        if 'arrays' in problem and isinstance(problem['arrays'], (list, tuple)) and len(problem['arrays']) >= 2:
            a, b = problem['arrays'][0], problem['arrays'][1]

        # Common aliases
        key_pairs = [
            ('a', 'b'),
            ('A', 'B'),
            ('array1', 'array2'),
            ('x', 'h'),
            ('signal', 'kernel'),
            ('seq1', 'seq2'),
            ('s1', 's2'),
            ('p', 'q'),
            ('poly1', 'poly2'),
            ('coeffs1', 'coeffs2'),
            ('data1', 'data2'),
            ('u', 'v'),
            ('input', 'filter'),
        ]
        for k1, k2 in key_pairs:
            if a is None and k1 in problem and k2 in problem:
                a, b = problem[k1], problem[k2]
                break

        # Fallback: pick the first two list-like numeric arrays
        if a is None or b is None:
            seqs = []
            for v in problem.values():
                if isinstance(v, (list, tuple)) and self._is_numeric_list(v):
                    seqs.append(v)
            if len(seqs) >= 2:
                a, b = seqs[0], seqs[1]

        a = self._to_list(a)
        b = self._to_list(b)

        cfg = {}
        # mode: full/same/valid/circular
        mode = problem.get('mode', 'full')
        if isinstance(mode, str):
            mode = mode.lower()
        cfg['mode'] = mode if mode in (
            'full', 'same', 'valid', 'circular') else 'full'

        # circular length
        n = problem.get('n') or problem.get('length') or problem.get('N')
        cfg['circular_length'] = int(n) if n is not None else None

        # modulo arithmetic
        cfg['mod'] = problem.get('mod', None)

        # integer rounding preference
        cfg['integer'] = problem.get('integer', None)
        cfg['round'] = problem.get('round', None)

        return a, b, cfg

    def _is_numeric_list(self, arr):
        if not isinstance(arr, (list, tuple)):
            return False
        for x in arr:
            if not isinstance(x, (int, float, complex)):
                return False
        return True

    def _to_list(self, arr):
        if isinstance(arr, (list, tuple)):
            return list(arr)
        return None

    def _all_ints(self, arr):
        if not isinstance(arr, list):
            return False
        for x in arr:
            if not isinstance(x, int):
                return False
        return True

    def _next_power_of_two(self, n):
        if n <= 1:
            return 1
        p = 1
        while p < n:
            p <<= 1
        return p

    def _fft_convolution_numpy(self, a, b, mode, circular_length, mod, keep_integer):
        import numpy as np

        # Handle empty inputs
        if not a or not b:
            return []

        a_np = np.asarray(a, dtype=float)
        b_np = np.asarray(b, dtype=float)

        if mode == 'circular':
            N = circular_length if circular_length is not None else max(
                len(a), len(b))
            N = int(N)
            if N <= 0:
                return []
            # zero-pad or truncate to N for circular conv
            if len(a) < N:
                a_np = np.pad(a_np, (0, N - len(a)))
            else:
                a_np = a_np[:N]
            if len(b) < N:
                b_np = np.pad(b_np, (0, N - len(b)))
            else:
                b_np = b_np[:N]

            fa = np.fft.rfft(a_np, n=N)
            fb = np.fft.rfft(b_np, n=N)
            yc = np.fft.irfft(fa * fb, n=N)
            y = yc
        else:
            # Linear convolution via FFT
            n_full = len(a) + len(b) - 1
            L = self._next_power_of_two(n_full)
            fa = np.fft.rfft(a_np, n=L)
            fb = np.fft.rfft(b_np, n=L)
            yc = np.fft.irfft(fa * fb, n=L)[:n_full]
            y = yc

            if mode == 'same':
                m, n = len(a), len(b)
                start = (n - 1) // 2
                y = y[start:start + m]
            elif mode == 'valid':
                m, n = len(a), len(b)
                start = min(m, n) - 1
                end = max(m, n)
                y = y[start:end]

        # Post-process: rounding and modulo
        if keep_integer or mod is not None:
            y = np.rint(y).astype(np.int64)
            if mod is not None:
                try:
                    m = int(mod)
                    if m > 0:
                        y %= m
                except Exception:
                    pass
            return y.tolist()
        else:
            # float output; trim very small values
            y = np.where(np.abs(y) < 1e-12, 0.0, y)
            return y.astype(float).tolist()

    def _fft_iterative(self, a, invert=False):
        # Iterative Cooley-Tukey FFT for power-of-two length
        import math
        import cmath
        n = len(a)
        j = 0
        # bit reversal
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
            ang = 2 * math.pi / length * (-1 if not invert else 1)
            wlen = complex(math.cos(ang), math.sin(ang))
            for i in range(0, n, length):
                w = 1 + 0j
                half = length // 2
                for k in range(half):
                    u = a[i + k]
                    v = a[i + k + half] * w
                    a[i + k] = u + v
                    a[i + k + half] = u - v
                    w *= wlen
            length <<= 1
        if invert:
            for i in range(n):
                a[i] /= n
        return a

    def _fft_convolution_pure(self, a, b, mode, circular_length, mod, keep_integer):
        # Handle empty inputs
        if not a or not b:
            return []

        # Prepare sequences
        import math
        m, n = len(a), len(b)

        if mode == 'circular':
            N = circular_length if circular_length is not None else max(m, n)
            N = int(N)
            if N <= 0:
                return []
            A = [0.0] * N
            B = [0.0] * N
            for i in range(min(m, N)):
                A[i] = float(a[i])
            for i in range(min(n, N)):
                B[i] = float(b[i])
            L = self._next_power_of_two(N)
            A += [0.0] * (L - N)
            B += [0.0] * (L - N)

            FA = self._fft_iterative([complex(x, 0.0)
                                     for x in A], invert=False)
            FB = self._fft_iterative([complex(x, 0.0)
                                     for x in B], invert=False)
            FC = [FA[i] * FB[i] for i in range(L)]
            yc = self._fft_iterative(FC, invert=True)
            y = [yc[i].real for i in range(N)]
        else:
            full_len = m + n - 1
            L = self._next_power_of_two(full_len)
            A = [0.0] * L
            B = [0.0] * L
            for i in range(m):
                A[i] = float(a[i])
            for i in range(n):
                B[i] = float(b[i])

            FA = self._fft_iterative([complex(x, 0.0)
                                     for x in A], invert=False)
            FB = self._fft_iterative([complex(x, 0.0)
                                     for x in B], invert=False)
            FC = [FA[i] * FB[i] for i in range(L)]
            yc = self._fft_iterative(FC, invert=True)
            yfull = [yc[i].real for i in range(full_len)]

            if mode == 'full':
                y = yfull
            elif mode == 'same':
                start = (n - 1) // 2
                y = yfull[start:start + m]
            elif mode == 'valid':
                start = min(m, n) - 1
                end = max(m, n)
                y = yfull[start:end]
            else:
                y = yfull

        # Post-process: rounding and modulo
        if keep_integer or mod is not None:
            y = [int(round(v)) for v in y]
            if mod is not None:
                try:
                    mm = int(mod)
                    if mm > 0:
                        y = [val % mm for val in y]
                except Exception:
                    pass
            return y
        else:
            return [0.0 if abs(v) < 1e-12 else float(v) for v in y]

    def _convolve(self, a, b, cfg):
        mode = cfg.get('mode', 'full')
        circular_length = cfg.get('circular_length', None)
        mod = cfg.get('mod', None)

        # Keep integer outputs if inputs all ints or explicitly requested
        keep_integer = cfg.get('integer', None)
        if keep_integer is None:
            keep_integer = self._all_ints(a) and self._all_ints(b)
        if cfg.get('round', None) is True:
            keep_integer = True

        if self._np_available:
            try:
                return self._fft_convolution_numpy(a, b, mode, circular_length, mod, keep_integer)
            except Exception:
                pass
        return self._fft_convolution_pure(a, b, mode, circular_length, mod, keep_integer)
