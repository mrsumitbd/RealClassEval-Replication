class FFTConvolution:
    '''
    Initial implementation of fft_convolution task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTConvolution.'''
        self._eps = 1e-9
        self._np = None
        try:
            import numpy as _np_mod
            self._np = _np_mod
        except Exception:
            self._np = None

    def _extract_sequences(self, problem):
        # Try common key pairs
        key_pairs = [
            ('a', 'b'),
            ('x', 'h'),
            ('signal', 'kernel'),
            ('array1', 'array2'),
            ('seq1', 'seq2'),
            ('input', 'weights'),
        ]
        for k1, k2 in key_pairs:
            if k1 in problem and k2 in problem:
                return problem[k1], problem[k2]
        # Fallback: find first two list-like entries
        seqs = []
        for v in problem.values():
            if isinstance(v, (list, tuple)):
                seqs.append(v)
            elif self._np is not None and isinstance(v, self._np.ndarray):
                seqs.append(v)
            if len(seqs) == 2:
                return seqs[0], seqs[1]
        raise ValueError(
            'Problem must contain two sequences (e.g., keys "a" and "b").')

    def _mode_from_problem(self, problem):
        mode = problem.get('mode', 'full')
        mode = str(mode).lower()
        if mode not in ('full', 'same', 'valid'):
            raise ValueError(f'Unsupported mode: {mode}')
        return mode

    def _to_array(self, seq):
        if self._np is not None:
            return self._np.asarray(seq, dtype=float)
        # Fallback to list of floats
        return [float(x) for x in seq]

    def _next_pow2(self, n):
        if n <= 1:
            return 1
        p = 1
        while p < n:
            p <<= 1
        return p

    def _convolve_naive_full(self, a, b):
        la = len(a)
        lb = len(b)
        if la == 0 or lb == 0:
            return []
        out_len = la + lb - 1
        out = [0.0] * out_len
        for i in range(la):
            ai = float(a[i])
            for j in range(lb):
                out[i + j] += ai * float(b[j])
        return out

    def _slice_mode(self, full, la, lb, mode):
        if mode == 'full':
            return full
        full_len = la + lb - 1
        if mode == 'same':
            out_len = max(la, lb)
            start = (full_len - out_len) // 2
            end = start + out_len
            return full[start:end]
        # mode == 'valid'
        out_len = max(0, abs(la - lb) + 1)
        if out_len == 0:
            return []
        start = min(la, lb) - 1
        end = start + out_len
        return full[start:end]

    def _fft_conv_full(self, a, b):
        la = len(a)
        lb = len(b)
        if la == 0 or lb == 0:
            return []
        if self._np is None:
            return self._convolve_naive_full(a, b)
        np = self._np
        n = la + lb - 1
        nfft = self._next_pow2(n)
        fa = np.fft.rfft(a, nfft)
        fb = np.fft.rfft(b, nfft)
        fc = fa * fb
        conv = np.fft.irfft(fc, nfft)[:n]
        return conv

    def _maybe_int_cast(self, seq):
        # Convert to Python list and cast to int if close
        if self._np is not None and isinstance(seq, self._np.ndarray):
            arr = seq
            if arr.size == 0:
                return []
            if self._np.all(self._np.isfinite(arr)) and self._np.all(self._np.abs(arr - self._np.round(arr)) < 1e-12):
                return [int(round(x)) for x in arr.tolist()]
            return arr.tolist()
        # seq is list
        if not seq:
            return []
        all_close = True
        for x in seq:
            if not (abs(x - round(x)) < 1e-12):
                all_close = False
                break
        if all_close:
            return [int(round(x)) for x in seq]
        return [float(x) for x in seq]

    def solve(self, problem):
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
        Returns:
            The solution in the format expected by the task
        '''
        a_raw, b_raw = self._extract_sequences(problem)
        mode = self._mode_from_problem(problem)
        a = self._to_array(a_raw)
        b = self._to_array(b_raw)

        # Convert to flat list/array for consistent operations
        if self._np is not None:
            a_arr = self._np.asarray(a, dtype=float)
            b_arr = self._np.asarray(b, dtype=float)
            la, lb = int(a_arr.size), int(b_arr.size)
            full = self._fft_conv_full(a_arr, b_arr)
            result = self._slice_mode(full, la, lb, mode)
        else:
            a_list = [float(x) for x in a]
            b_list = [float(x) for x in b]
            la, lb = len(a_list), len(b_list)
            full = self._convolve_naive_full(a_list, b_list)
            result = self._slice_mode(full, la, lb, mode)

        return self._maybe_int_cast(result)

    def _extract_solution_array(self, solution):
        # Accept either a raw list/array or dict with 'result' key
        if isinstance(solution, dict):
            if 'result' in solution:
                return solution['result']
            # Try generic key
            for k in ('convolution', 'conv', 'output'):
                if k in solution:
                    return solution[k]
            # If dict has a single list-like value, use it
            values = [v for v in solution.values(
            ) if isinstance(v, (list, tuple))]
            if not values and self._np is not None:
                values = [v for v in solution.values(
                ) if isinstance(v, self._np.ndarray)]
            if len(values) == 1:
                return values[0]
        return solution

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        provided = self._extract_solution_array(solution)

        if 'expected' in problem:
            expected = problem['expected']
        else:
            expected = self.solve(problem)

        # Convert to numpy arrays for comparison if available
        if self._np is not None:
            np = self._np
            exp = np.asarray(expected, dtype=float)
            prov = np.asarray(provided, dtype=float)
            if exp.shape != prov.shape:
                return False
            if exp.size == 0 and prov.size == 0:
                return True
            return np.allclose(exp, prov, atol=max(self._eps, 1e-9), rtol=0)
        # Fallback comparison
        exp_list = [float(x) for x in expected] if isinstance(
            expected, (list, tuple)) else []
        prov_list = [float(x) for x in provided] if isinstance(
            provided, (list, tuple)) else []
        if len(exp_list) != len(prov_list):
            return False
        for x, y in zip(exp_list, prov_list):
            if abs(x - y) > max(self._eps, 1e-9):
                return False
        return True
