import numpy as np


class FFTConvolution:
    '''
    Initial implementation of fft_convolution task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTConvolution.'''
        pass

    @staticmethod
    def _next_pow2(n: int) -> int:
        if n <= 1:
            return 1
        return 1 << (int(n - 1).bit_length())

    @staticmethod
    def _fft_convolve_linear_1d(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        n = a.size
        m = b.size
        if n == 0 or m == 0:
            raise ValueError("convolve: inputs cannot be empty")
        nconv = n + m - 1
        nfft = FFTConvolution._next_pow2(nconv)

        real_input = np.isrealobj(a) and np.isrealobj(b)
        if real_input:
            fa = np.fft.rfft(a, nfft)
            fb = np.fft.rfft(b, nfft)
            y = np.fft.irfft(fa * fb, nfft)[:nconv]
        else:
            fa = np.fft.fft(a, nfft)
            fb = np.fft.fft(b, nfft)
            y = np.fft.ifft(fa * fb, nfft)[:nconv]

        return y

    @staticmethod
    def _crop_mode_from_full(y_full: np.ndarray, n: int, m: int, mode: str) -> np.ndarray:
        mode = mode.lower()
        if mode == 'full':
            return y_full
        elif mode == 'same':
            L_full = n + m - 1
            L_same = max(n, m)
            start = (L_full - L_same) // 2
            end = start + L_same
            return y_full[start:end]
        elif mode == 'valid':
            L_valid = max(n, m) - min(n, m) + 1
            start = min(n, m) - 1
            end = start + L_valid
            return y_full[start:end]
        else:
            raise ValueError(f"Unsupported mode: {mode}")

    @staticmethod
    def _fft_convolve_circular_1d(a: np.ndarray, b: np.ndarray, n: int | None = None) -> np.ndarray:
        if n is None:
            n = max(a.size, b.size)
        if n <= 0:
            raise ValueError("circular convolution length must be positive")

        a_pad = np.zeros(n, dtype=np.result_type(
            a.dtype, np.float64 if a.dtype.kind in "iu" else a.dtype))
        b_pad = np.zeros(n, dtype=np.result_type(
            b.dtype, np.float64 if b.dtype.kind in "iu" else b.dtype))
        a_pad[:min(a.size, n)] = a[:min(a.size, n)]
        b_pad[:min(b.size, n)] = b[:min(b.size, n)]

        real_input = np.isrealobj(a) and np.isrealobj(b)
        if real_input:
            fa = np.fft.rfft(a_pad, n)
            fb = np.fft.rfft(b_pad, n)
            y = np.fft.irfft(fa * fb, n)
        else:
            fa = np.fft.fft(a_pad, n)
            fb = np.fft.fft(b_pad, n)
            y = np.fft.ifft(fa * fb, n)

        return y

    @staticmethod
    def _to_numpy_1d(x):
        arr = np.asarray(x)
        if arr.ndim != 1:
            raise ValueError("Inputs must be 1D sequences")
        return arr

    @staticmethod
    def _maybe_realify(y: np.ndarray) -> np.ndarray:
        if np.iscomplexobj(y):
            imag_max = np.max(np.abs(y.imag)) if y.size else 0.0
            if imag_max < 1e-10:
                return y.real
        return y

    def solve(self, problem):
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
        Returns:
            The solution in the format expected by the task
        '''
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dict")

        if 'a' not in problem or 'b' not in problem:
            raise KeyError("problem must contain 'a' and 'b' sequences")

        a = self._to_numpy_1d(problem['a'])
        b = self._to_numpy_1d(problem['b'])

        mode = problem.get('mode', 'full')
        circular = bool(problem.get('circular', False))
        n_circ = problem.get('n') or problem.get(
            'size')  # optional for circular

        # Promote integer arrays to float for FFT stability
        if a.dtype.kind in "iu":
            a = a.astype(np.float64)
        if b.dtype.kind in "iu":
            b = b.astype(np.float64)

        if circular:
            y = self._fft_convolve_circular_1d(a, b, n_circ)
        else:
            y_full = self._fft_convolve_linear_1d(a, b)
            y = self._crop_mode_from_full(y_full, a.size, b.size, mode)

        y = self._maybe_realify(y)

        # Return as list by default to be broadly compatible
        return y.tolist()

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
            if not isinstance(problem, dict):
                return False
            if 'a' not in problem or 'b' not in problem:
                return False

            a = self._to_numpy_1d(problem['a'])
            b = self._to_numpy_1d(problem['b'])
            circular = bool(problem.get('circular', False))

            # Normalize solution to numpy array
            y_sol = np.asarray(solution)
            if y_sol.ndim != 1:
                return False

            if circular:
                n_circ = problem.get('n') or problem.get('size')
                n = n_circ if n_circ is not None else max(a.size, b.size)
                y_ref = self._fft_convolve_circular_1d(a.astype(np.complex128, copy=False),
                                                       b.astype(
                                                           np.complex128, copy=False),
                                                       n=n)
            else:
                mode = problem.get('mode', 'full')
                # Use numpy.convolve for reference to match exact 'same'/'valid' semantics
                y_ref = np.convolve(a.astype(np.complex128, copy=False),
                                    b.astype(np.complex128, copy=False),
                                    mode=mode)

            y_ref = self._maybe_realify(y_ref)
            y_sol = self._maybe_realify(y_sol.astype(y_ref.dtype, copy=False))

            if y_ref.shape != y_sol.shape:
                return False

            return np.allclose(y_ref, y_sol, rtol=1e-7, atol=1e-8, equal_nan=False)
        except Exception:
            return False
