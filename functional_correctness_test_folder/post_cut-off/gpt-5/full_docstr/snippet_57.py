class FFTConvolution:
    '''
    Initial implementation of fft_convolution task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTConvolution.'''
        try:
            import numpy as _np  # noqa: F401
            self._has_numpy = True
        except Exception:
            self._has_numpy = False

    def _extract_sequences(self, problem):
        # Try common key names
        keys_a = ['a', 'x', 'signal', 'seq1', 'input', 'data']
        keys_b = ['b', 'h', 'kernel', 'seq2', 'filter', 'weights']
        a = b = None
        for k in keys_a:
            if k in problem:
                a = problem[k]
                break
        for k in keys_b:
            if k in problem:
                b = problem[k]
                break
        # If still None, try tuple under 'sequences' or 'pair'
        if a is None or b is None:
            if 'sequences' in problem and isinstance(problem['sequences'], (list, tuple)) and len(problem['sequences']) >= 2:
                a, b = problem['sequences'][:2]
            elif 'pair' in problem and isinstance(problem['pair'], (list, tuple)) and len(problem['pair']) >= 2:
                a, b = problem['pair'][:2]
        if a is None or b is None:
            raise ValueError(
                "Problem must contain two sequences (e.g., keys 'a' and 'b' or 'signal' and 'kernel').")
        # Convert to list
        a = list(a)
        b = list(b)
        return a, b

    def _get_mode(self, problem):
        mode = problem.get('mode', 'full')
        if mode not in ('full', 'same', 'valid'):
            # accept some variants
            m = str(mode).lower()
            if m in ('f', 'full'):
                mode = 'full'
            elif m in ('s', 'same'):
                mode = 'same'
            elif m in ('v', 'valid'):
                mode = 'valid'
            else:
                mode = 'full'
        return mode

    def _is_complex(self, seq):
        for v in seq:
            if isinstance(v, complex):
                return True
        return False

    def _to_numpy(self, seq):
        import numpy as np
        # choose dtype
        if self._is_complex(seq):
            return np.asarray(seq, dtype=np.complex128)
        # detect floats
        has_float = any(isinstance(v, float) for v in seq)
        dtype = np.float64 if has_float else np.float64
        return np.asarray(seq, dtype=dtype)

    def _next_pow2(self, n):
        if n <= 1:
            return 1
        p = 1
        while p < n:
            p <<= 1
        return p

    def _fft_convolve_full(self, a, b):
        # FFT-based full convolution if numpy available; else direct
        if not self._has_numpy:
            return self._direct_convolve_full(a, b)
        import numpy as np
        n = len(a)
        m = len(b)
        if n == 0 or m == 0:
            return []
        A = self._to_numpy(a)
        B = self._to_numpy(b)
        L = self._next_pow2(n + m - 1)
        FA = np.fft.rfft(A, n=L) if np.isrealobj(
            A) and np.isrealobj(B) else np.fft.fft(A, n=L)
        FB = np.fft.rfft(B, n=L) if np.isrealobj(
            A) and np.isrealobj(B) else np.fft.fft(B, n=L)
        FC = FA * FB
        if np.isrealobj(A) and np.isrealobj(B):
            c = np.fft.irfft(FC, n=L)
        else:
            c = np.fft.ifft(FC, n=L)
        c = c[: n + m - 1]
        # cast to real if imaginary part negligible
        if np.iscomplexobj(c):
            if np.max(np.abs(c.imag)) <= 1e-10:
                c = c.real
        return c.tolist()

    def _direct_convolve_full(self, a, b):
        n = len(a)
        m = len(b)
        if n == 0 or m == 0:
            return []
        # Support complex numbers
        res_len = n + m - 1
        res = [0] * res_len
        for i in range(n):
            ai = a[i]
            for j in range(m):
                res[i + j] += ai * b[j]
        return res

    def _mode_slice(self, full, n, m, mode):
        # Emulate numpy.convolve mode slicing with a as length n, b as length m
        if mode == 'full':
            return full
        if mode == 'same':
            # same length as a, centered
            pad = (m - 1) // 2
            start = pad
            end = start + n
            # For even kernel sizes, numpy centers to the right; this slicing matches numpy
            if (m % 2) == 0:
                start = (m // 2) - 1
                end = start + n
            return full[start:end]
        if mode == 'valid':
            if n < m:
                # numpy returns empty list
                return []
            start = m - 1
            end = start + (n - m + 1)
            return full[start:end]
        return full

    def _postprocess(self, seq, problem):
        # Rounding/precision handling
        precision = problem.get('precision', None)
        if precision is None:
            # default rounding to reduce tiny numerical noise
            precision = 10

        def maybe_round(x):
            if isinstance(x, complex):
                r = round(x.real, precision)
                im = round(x.imag, precision)
                if abs(im) <= 10**(-precision):
                    return r
                return complex(r, im)
            else:
                return round(x, precision)
        out = [maybe_round(v) for v in seq]
        # Optionally cast to int if requested
        cast_int = problem.get('cast_int', False)
        if cast_int:
            co = []
            for v in out:
                if isinstance(v, complex):
                    co.append(v)
                else:
                    vi = int(round(v))
                    co.append(vi)
            return co
        return out

    def solve(self, problem):
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
        Returns:
            The solution in the format expected by the task
        '''
        a, b = self._extract_sequences(problem)
        mode = self._get_mode(problem)
        full = self._fft_convolve_full(a, b)
        n = len(a)
        m = len(b)
        sliced = self._mode_slice(full, n, m, mode)
        result = self._postprocess(sliced, problem)
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
            a, b = self._extract_sequences(problem)
            mode = self._get_mode(problem)
            # Compute ground truth via direct convolution for robustness
            full = self._direct_convolve_full(a, b)
            expected = self._mode_slice(full, len(a), len(b), mode)
            # Compare numerically
            if len(expected) != len(solution):
                return False
            tol = problem.get('atol', 1e-6)
            # Normalize solution types to complex-capable for comparison
            for ev, sv in zip(expected, solution):
                # Convert to complex for uniform comparison
                if isinstance(ev, complex) or isinstance(sv, complex):
                    ev_c = complex(ev)
                    sv_c = complex(sv)
                    if abs(ev_c.real - sv_c.real) > tol or abs(ev_c.imag - sv_c.imag) > tol:
                        return False
                else:
                    try:
                        sv_f = float(sv)
                    except Exception:
                        return False
                    if abs(float(ev) - sv_f) > tol:
                        return False
            return True
        except Exception:
            return False
