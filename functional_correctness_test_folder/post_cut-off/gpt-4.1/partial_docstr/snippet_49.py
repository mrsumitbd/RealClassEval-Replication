
class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''
    @staticmethod
    def solve(problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
        Returns:
            The solution in the format expected by the task
        '''
        from scipy.fftpack import fft
        x = problem['input']
        # x is expected to be a list or numpy array of complex numbers
        result = fft(x)
        return result

    @staticmethod
    def is_solution(problem, solution):
        import numpy as np
        from scipy.fftpack import fft
        x = problem['input']
        expected = fft(x)
        return np.allclose(solution, expected)
