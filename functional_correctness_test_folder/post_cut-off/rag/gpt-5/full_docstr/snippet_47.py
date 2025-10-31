import numpy as np

try:
    from scipy.signal import fftconvolve as _fftconvolve
except Exception:
    _fftconvolve = None


class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the Convolve2DFullFill.'''
        self._fftconvolve = _fftconvolve

    def solve(self, problem):
        '''
        Compute the 2D convolution of arrays a and b using "full" mode and "fill" boundary.
        Uses scipy.signal.fftconvolve for efficiency, which implicitly handles "fill" boundary.
        Args:
            problem: A tuple (a, b) of 2D arrays.
        Returns:
            A 2D array containing the convolution result.
        '''
        if not isinstance(problem, (list, tuple)) or len(problem) != 2:
            raise ValueError("problem must be a tuple (a, b) of 2D arrays")
        a, b = problem
        a = np.asarray(a)
        b = np.asarray(b)

        if a.ndim != 2 or b.ndim != 2:
            raise ValueError("Both input arrays must be 2D")
        if 0 in a.shape or 0 in b.shape:
            raise ValueError("Input arrays must be non-empty")

        if self._fftconvolve is not None:
            return self._fftconvolve(a, b, mode='full')

        # Fallback: manual FFT-based 2D full convolution with zero padding.
        out_shape = (a.shape[0] + b.shape[0] - 1, a.shape[1] + b.shape[1] - 1)

        # Choose computation dtype
        comp_dtype = np.result_type(a.dtype, b.dtype, np.float64)
        a_c = a.astype(comp_dtype, copy=False)
        b_c = b.astype(comp_dtype, copy=False)

        if np.iscomplexobj(a_c) or np.iscomplexobj(b_c):
            FA = np.fft.fftn(a_c, out_shape)
            FB = np.fft.fftn(b_c, out_shape)
            out = np.fft.ifftn(FA * FB, out_shape)
        else:
            FA = np.fft.rfftn(a_c, out_shape)
            FB = np.fft.rfftn(b_c, out_shape)
            out = np.fft.irfftn(FA * FB, out_shape)

        # For numerical stability, if result is nearly real, return real
        if np.iscomplexobj(out):
            if np.max(np.abs(out.imag)) < 1e-12:
                out = out.real
        return out

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
            sol = np.asarray(solution)
            if expected.shape != sol.shape:
                return False
            if np.iscomplexobj(expected) or np.iscomplexobj(sol):
                return np.allclose(expected, sol, rtol=1e-7, atol=1e-9)
            return np.allclose(expected, sol, rtol=1e-7, atol=1e-9)
        except Exception:
            return False
