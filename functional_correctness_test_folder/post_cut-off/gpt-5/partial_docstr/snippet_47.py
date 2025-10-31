class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        pass

    def solve(self, problem):
        '''
        Compute the 2D convolution of arrays a and b using "full" mode and "fill" boundary.
        Uses FFT-based convolution which implicitly handles "fill" boundary.
        Args:
            problem: A tuple (a, b) of 2D arrays.
        Returns:
            A 2D array containing the convolution result.
        '''
        import numpy as np

        a, b = problem
        a = np.asarray(a)
        b = np.asarray(b)

        if a.ndim != 2 or b.ndim != 2:
            raise ValueError("Both inputs must be 2D arrays.")

        out_shape = (a.shape[0] + b.shape[0] - 1, a.shape[1] + b.shape[1] - 1)

        fa = np.fft.fft2(a, out_shape)
        fb = np.fft.fft2(b, out_shape)
        conv = np.fft.ifft2(fa * fb)

        if np.isrealobj(a) and np.isrealobj(b):
            conv = conv.real

        return conv

    def is_solution(self, problem, solution):
        import numpy as np

        a, b = problem
        a = np.asarray(a)
        b = np.asarray(b)
        sol = np.asarray(solution)

        if a.ndim != 2 or b.ndim != 2 or sol.ndim != 2:
            return False

        expected_shape = (a.shape[0] + b.shape[0] - 1,
                          a.shape[1] + b.shape[1] - 1)
        if sol.shape != expected_shape:
            return False

        # Naive full 2D convolution (fill with zeros)
        out = np.zeros(expected_shape, dtype=np.result_type(a, b, np.float64))
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                out[i:i + b.shape[0], j:j + b.shape[1]] += a[i, j] * b

        return np.allclose(sol, out, atol=1e-8, rtol=1e-5)
