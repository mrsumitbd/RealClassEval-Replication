import numpy as np

try:
    from scipy.signal import fftconvolve as _scipy_fftconvolve
except Exception:
    _scipy_fftconvolve = None


class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the Convolve2DFullFill.'''
        self._scipy_fftconvolve = _scipy_fftconvolve

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
            raise ValueError("problem must be a tuple (a, b) of 2D arrays")
        a, b = problem
        a = np.asarray(a)
        b = np.asarray(b)

        if a.ndim != 2 or b.ndim != 2:
            raise ValueError("Both input arrays must be 2D")

        # Handle empty inputs gracefully
        out_shape = (max(a.shape[0] + b.shape[0] - 1, 0),
                     max(a.shape[1] + b.shape[1] - 1, 0))
        if a.size == 0 or b.size == 0 or out_shape[0] == 0 or out_shape[1] == 0:
            # Return an empty array of appropriate shape and dtype
            if np.iscomplexobj(a) or np.iscomplexobj(b):
                out_dtype = np.result_type(a.dtype, b.dtype, np.complex128)
            else:
                out_dtype = np.result_type(a.dtype, b.dtype, np.float64)
            return np.zeros(out_shape, dtype=out_dtype)

        if self._scipy_fftconvolve is not None:
            res = self._scipy_fftconvolve(a, b, mode='full')
            return res

        # Fallback: manual FFT-based 2D convolution
        fshape = (a.shape[0] + b.shape[0] - 1, a.shape[1] + b.shape[1] - 1)

        # Choose computation dtype
        if np.iscomplexobj(a) or np.iscomplexobj(b):
            comp_dtype = np.result_type(a.dtype, b.dtype, np.complex128)
            want_complex = True
        else:
            comp_dtype = np.result_type(a.dtype, b.dtype, np.float64)
            want_complex = False

        Fa = np.fft.fftn(a.astype(comp_dtype, copy=False), fshape)
        Fb = np.fft.fftn(b.astype(comp_dtype, copy=False), fshape)
        conv = np.fft.ifftn(Fa * Fb)

        if not want_complex:
            conv = conv.real

        # Cast back to appropriate output dtype
        out_dtype = np.result_type(
            a.dtype, b.dtype, np.float64 if not want_complex else np.complex128)
        return conv.astype(out_dtype, copy=False)

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
        sol_arr = np.asarray(solution)
        if sol_arr.shape != expected.shape:
            return False
        # Use allclose to tolerate minor numerical differences
        return np.allclose(sol_arr, expected, rtol=1e-7, atol=1e-9, equal_nan=True)
