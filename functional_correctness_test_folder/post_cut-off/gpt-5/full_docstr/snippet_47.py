class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the Convolve2DFullFill.'''
        pass

    def solve(self, problem):
        '''
        Compute the 2D convolution of arrays a and b using "full" mode and "fill" boundary.
        Uses scipy.signal.fftconvolve for efficiency, which implicitly handles "fill" boundary.
        Args:
            problem: A tuple (a, b) of 2D arrays.
        Returns:
            A 2D array containing the convolution result.
        '''
        import numpy as np

        if not isinstance(problem, (tuple, list)) or len(problem) != 2:
            raise ValueError("problem must be a tuple (a, b) of 2D arrays")

        a, b = problem
        a = np.asarray(a)
        b = np.asarray(b)

        if a.ndim != 2 or b.ndim != 2:
            raise ValueError("Both inputs must be 2D arrays")
        if a.size == 0 or b.size == 0:
            raise ValueError("Inputs must be non-empty")

        out_shape = (a.shape[0] + b.shape[0] - 1, a.shape[1] + b.shape[1] - 1)

        is_complex = np.iscomplexobj(a) or np.iscomplexobj(b)

        if is_complex:
            FA = np.fft.fftn(a, s=out_shape)
            FB = np.fft.fftn(b, s=out_shape)
            conv = np.fft.ifftn(FA * FB)
            return conv
        else:
            FA = np.fft.rfftn(a, s=out_shape)
            FB = np.fft.rfftn(b, s=out_shape)
            conv = np.fft.irfftn(FA * FB, s=out_shape)
            return conv

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        import numpy as np

        try:
            a, b = problem
        except Exception:
            return False

        a = np.asarray(a)
        b = np.asarray(b)
        sol = np.asarray(solution)

        if a.ndim != 2 or b.ndim != 2 or sol.ndim != 2:
            return False

        expected_shape = (a.shape[0] + b.shape[0] - 1,
                          a.shape[1] + b.shape[1] - 1)
        if sol.shape != expected_shape:
            return False

        try:
            expected = self.solve((a, b))
        except Exception:
            return False

        return np.allclose(sol, expected, rtol=1e-7, atol=1e-9)
