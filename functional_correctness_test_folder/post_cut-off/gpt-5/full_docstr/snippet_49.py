class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''
    @staticmethod
    def _get_backend():
        try:
            from scipy.fftpack import fft as sc_fft, ifft as sc_ifft
            return sc_fft, sc_ifft, 'scipy'
        except Exception:
            try:
                from numpy.fft import fft as np_fft, ifft as np_ifft
                return np_fft, np_ifft, 'numpy'
            except Exception:
                return None, None, None

    @staticmethod
    def _get_signal(problem):
        for key in ('signal', 'data', 'x', 'input'):
            if key in problem:
                return problem[key]
        raise ValueError(
            "No input signal found in problem. Expected one of: 'signal', 'data', 'x', 'input'.")

    @staticmethod
    def _get_operation(problem):
        # Determine operation: 'fft' or 'ifft'
        if 'op' in problem and problem['op'] is not None:
            op = str(problem['op']).lower()
            if op in ('fft', 'ifft'):
                return op
        if 'operation' in problem and problem['operation'] is not None:
            op = str(problem['operation']).lower()
            if op in ('fft', 'ifft'):
                return op
        # Fallback via boolean inverse flag
        inv = problem.get('inverse', False)
        return 'ifft' if inv else 'fft'

    @staticmethod
    def solve(problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
        Returns:
            The solution in the format expected by the task
        '''
        import numpy as np

        fft_func, ifft_func, _ = FFTComplexScipyFFTpack._get_backend()
        if fft_func is None or ifft_func is None:
            raise RuntimeError(
                "No FFT backend available. Ensure SciPy or NumPy is installed.")

        x = FFTComplexScipyFFTpack._get_signal(problem)
        arr = np.asarray(x)

        # Ensure complex dtype if indicated or if complex present
        if np.iscomplexobj(arr):
            pass
        else:
            # If explicitly requested complex input
            force_complex = problem.get('complex', False)
            if force_complex:
                arr = arr.astype(np.complex128, copy=False)

        op = FFTComplexScipyFFTpack._get_operation(problem)
        n = problem.get('n', None)
        axis = problem.get('axis', -1)
        norm = problem.get('norm', None)
        # scipy.fftpack/numpy.fft have norm parameter for numpy >=1.20; fftpack's fft does not accept norm.
        # We adapt: If backend is numpy, pass norm; else ignore norm.
        if op == 'fft':
            try:
                res = fft_func(arr, n=n, axis=axis, norm=norm)
            except TypeError:
                res = fft_func(arr, n=n, axis=axis)
        else:
            try:
                res = ifft_func(arr, n=n, axis=axis, norm=norm)
            except TypeError:
                res = ifft_func(arr, n=n, axis=axis)

        # Output as nested lists with complex numbers represented natively (Python complex)
        return np.asarray(res).tolist()

    @staticmethod
    def is_solution(problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        import numpy as np

        # If expected provided in problem, compare directly
        if 'expected' in problem and problem['expected'] is not None:
            expected = np.asarray(problem['expected'])
        else:
            try:
                computed = FFTComplexScipyFFTpack.solve(problem)
            except Exception:
                return False
            expected = np.asarray(computed)

        sol_arr = np.asarray(solution)

        # Shape check (allow broadcasting only if exactly equal)
        if expected.shape != sol_arr.shape:
            return False

        # Comparison tolerances
        atol = problem.get('atol', 1e-8)
        rtol = problem.get('rtol', 1e-7)

        # Handle complex comparisons
        try:
            return np.allclose(sol_arr, expected, rtol=rtol, atol=atol, equal_nan=True)
        except Exception:
            # If solution contains non-numeric entries
            return False
