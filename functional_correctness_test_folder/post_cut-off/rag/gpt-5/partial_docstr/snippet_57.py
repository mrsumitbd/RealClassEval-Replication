import numpy as np


class FFTConvolution:
    '''
    Initial implementation of fft_convolution task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTConvolution.'''
        self.default_mode = 'full'
        self.atol = 1e-8
        self.rtol = 1e-5

    def _extract_sequences(self, problem):
        # Try multiple common keys to locate the input sequences.
        candidates_a = ['a', 'x', 'signal', 'seq1', 'input', 'data']
        candidates_b = ['b', 'h', 'kernel', 'seq2', 'filter', 'impulse']
        a = None
        b = None
        for k in candidates_a:
            if k in problem:
                a = problem[k]
                break
        for k in candidates_b:
            if k in problem:
                b = problem[k]
                break
        if a is None or b is None:
            raise ValueError(
                "Problem must contain two sequences (e.g., keys 'a' and 'b').")
        return a, b

    def _extract_mode_and_n(self, problem):
        mode = problem.get('mode', self.default_mode)
        if mode not in ('full', 'same', 'valid', 'circular'):
            # Be lenient with synonyms
            m = str(mode).lower()
            if m in ('full', 'same', 'valid', 'circular'):
                mode = m
            else:
                raise ValueError(f"Unsupported mode: {mode}")
        n = problem.get('n', problem.get('length', None))
        return mode, n

    def _to_array(self, seq):
        arr = np.asarray(seq)
        if arr.ndim != 1:
            arr = np.ravel(arr)
        # Choose dtype
        if np.iscomplexobj(arr):
            return arr.astype(np.complex128, copy=False)
        return arr.astype(np.float64, copy=False)

    def _next_pow2(self, n):
        if n <= 1:
            return 1
        return 1 << (n - 1).bit_length()

    def _fft_full_convolution(self, a, b):
        la = a.shape[0]
        lb = b.shape[0]
        n_full = la + lb - 1
        L = self._next_pow2(n_full)
        use_complex = np.iscomplexobj(a) or np.iscomplexobj(b)
        if use_complex:
            fa = np.fft.fft(a, L)
            fb = np.fft.fft(b, L)
            c = np.fft.ifft(fa * fb)[:n_full]
        else:
            fa = np.fft.rfft(a, L)
            fb = np.fft.rfft(b, L)
            c = np.fft.irfft(fa * fb, L)[:n_full]
        return np.real_if_close(c, tol=1000)

    def _linear_convolution(self, a, b, mode):
        c_full = self._fft_full_convolution(a, b)
        la = a.shape[0]
        lb = b.shape[0]
        if mode == 'full':
            return c_full
        if mode == 'same':
            # Numpy semantics: same size as first input (a), centered
            start = (lb - 1) // 2
            end = start + la
            return c_full[start:end]
        if mode == 'valid':
            # Indices from min(la, lb)-1 to max(la, lb)-1 inclusive
            start = min(la, lb) - 1
            end = max(la, lb)
            if end <= start:
                # No valid overlap
                return c_full[0:0]
            return c_full[start:end]
        raise ValueError(f"Unsupported mode: {mode}")

    def _circular_convolution(self, a, b, n=None):
        la = a.shape[0]
        lb = b.shape[0]
        if n is None:
            n = max(la, lb)
        use_complex = np.iscomplexobj(a) or np.iscomplexobj(b)
        if use_complex:
            fa = np.fft.fft(a, n)
            fb = np.fft.fft(b, n)
            c = np.fft.ifft(fa * fb)
        else:
            fa = np.fft.rfft(a, n)
            fb = np.fft.rfft(b, n)
            c = np.fft.irfft(fa * fb, n)
        return np.real_if_close(c, tol=1000)

    def _prepare_output(self, arr):
        # Convert to Python list; cast very small imaginary parts away if applicable.
        arr = np.real_if_close(arr, tol=1000)
        if np.iscomplexobj(arr):
            return [complex(x) for x in arr.tolist()]
        return [float(x) for x in arr.tolist()]

    def solve(self, problem):
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
        Returns:
            The solution in the format expected by the task
        '''
        a_raw, b_raw = self._extract_sequences(problem)
        a = self._to_array(a_raw)
        b = self._to_array(b_raw)

        if a.size == 0 or b.size == 0:
            raise ValueError("Input sequences must be non-empty.")

        mode, n = self._extract_mode_and_n(problem)

        if mode == 'circular':
            result = self._circular_convolution(a, b, n=n)
        else:
            result = self._linear_convolution(a, b, mode)

        return self._prepare_output(result)

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Extract proposed result from various possible formats
        if isinstance(solution, dict):
            for key in ('result', 'output', 'convolution', 'y'):
                if key in solution:
                    proposed = solution[key]
                    break
            else:
                return False
        else:
            proposed = solution

        try:
            expected = self.solve(problem)
        except Exception:
            return False

        try:
            proposed_arr = np.asarray(proposed)
        except Exception:
            return False

        expected_arr = np.asarray(expected)

        if proposed_arr.shape != expected_arr.shape:
            return False

        # Handle real vs complex comparison
        if np.iscomplexobj(expected_arr) or np.iscomplexobj(proposed_arr):
            # Compare both real and imaginary parts
            real_close = np.allclose(
                proposed_arr.real, expected_arr.real, rtol=self.rtol, atol=self.atol, equal_nan=False)
            imag_close = np.allclose(
                proposed_arr.imag, expected_arr.imag, rtol=self.rtol, atol=self.atol, equal_nan=False)
            return bool(real_close and imag_close)
        else:
            return bool(np.allclose(proposed_arr.astype(float), expected_arr.astype(float), rtol=self.rtol, atol=self.atol, equal_nan=False))
