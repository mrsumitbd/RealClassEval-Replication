import numpy as np


class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the Convolve2DFullFill.'''
        try:
            from scipy.signal import fftconvolve as _fftconvolve  # type: ignore
        except Exception:  # pragma: no cover
            _fftconvolve = None
        self._scipy_fftconvolve = _fftconvolve
        self._rtol = 1e-7
        self._atol = 1e-9

    def _numpy_fft_conv2d(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        # Determine output shape for 'full' convolution
        out_shape = (a.shape[0] + b.shape[0] - 1, a.shape[1] + b.shape[1] - 1)
        # Select computation dtype to avoid overflow and to handle complex inputs
        comp_dtype = np.result_type(a.dtype, b.dtype, np.float64)
        a_z = np.asarray(a, dtype=comp_dtype)
        b_z = np.asarray(b, dtype=comp_dtype)
        # FFT-based linear convolution via zero-padding
        Fa = np.fft.fftn(a_z, s=out_shape)
        Fb = np.fft.fftn(b_z, s=out_shape)
        conv = np.fft.ifftn(Fa * Fb)
        # If inputs are real, discard tiny imaginary parts
        if not (np.iscomplexobj(a) or np.iscomplexobj(b)):
            conv = conv.real
        return conv

    def solve(self, problem):
        '''
        Compute the 2D convolution of arrays a and b using "full" mode and "fill" boundary.
        Uses scipy.signal.fftconvolve for efficiency, which implicitly handles "fill" boundary.
        Args:
            problem: A tuple (a, b) of 2D arrays.
        Returns:
            A 2D array containing the convolution result.
        '''
        if not isinstance(problem, (tuple, list)) or len(problem) != 2:
            raise ValueError("problem must be a (a, b) tuple of 2D arrays")
        a = np.asarray(problem[0])
        b = np.asarray(problem[1])

        if a.ndim != 2 or b.ndim != 2:
            raise ValueError("Both inputs must be 2D arrays")
        if a.size == 0 or b.size == 0:
            raise ValueError("Input arrays must be non-empty")

        if self._scipy_fftconvolve is not None:
            # Use SciPy if available
            return self._scipy_fftconvolve(a, b, mode='full')
        # Fallback: NumPy FFT implementation
        return self._numpy_fft_conv2d(a, b)

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
            a = np.asarray(problem[0])
            b = np.asarray(problem[1])
        except Exception:
            return False

        if a.ndim != 2 or b.ndim != 2:
            return False
        if a.size == 0 or b.size == 0:
            return False

        sol = np.asarray(solution)
        if sol.ndim != 2:
            return False

        try:
            expected = self.solve(problem)
        except Exception:
            return False

        if sol.shape != expected.shape:
            return False

        # Compare with tolerance for floating-point outputs
        if np.iscomplexobj(expected) or np.iscomplexobj(sol):
            return np.allclose(sol, expected, rtol=self._rtol, atol=self._atol)
        else:
            return np.allclose(sol, expected, rtol=self._rtol, atol=self._atol)
