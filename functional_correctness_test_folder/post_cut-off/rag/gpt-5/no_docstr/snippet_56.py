import numpy as np


class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTComplexScipyFFTpack.'''
        self._use_scipy = False
        self._fft = None
        self._ifft = None
        try:
            import scipy.fftpack as sp_fftpack  # type: ignore
            self._fft = sp_fftpack.fft
            self._ifft = sp_fftpack.ifft
            self._use_scipy = True
        except Exception:
            self._fft = np.fft.fft
            self._ifft = np.fft.ifft
            self._use_scipy = False

    def _extract_input_array(self, problem):
        for key in ('x', 'input', 'signal', 'data', 'array', 'a', 'values'):
            if key in problem:
                arr = problem[key]
                return np.asarray(arr)
        raise ValueError(
            'Problem dictionary must contain input array under one of keys: x, input, signal, data, array, a, values')

    def _effective_n(self, x, n, axis):
        if n is None:
            ax = axis if axis is not None else -1
            ax = ax if ax >= 0 else x.ndim + ax
            return x.shape[ax]
        return int(n)

    def _apply_norm_scaling(self, y, n_eff, inverse, norm):
        if norm is None or norm == 'backward':
            return y
        if norm == 'ortho':
            scale = 1.0 / np.sqrt(float(n_eff))
            if inverse:
                # backend inverse is already divided by n -> need multiply by sqrt(n)
                return y * np.sqrt(float(n_eff))
            else:
                # forward unnormalized -> divide by sqrt(n)
                return y * scale
        if norm == 'forward':
            if inverse:
                # backend inverse divides by n, but 'forward' expects unnormalized inverse
                return y * float(n_eff)
            else:
                # forward should be normalized by 1/n
                return y / float(n_eff)
        # If norm is unrecognized, return as-is
        return y

    def solve(self, problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
        Returns:
            The solution in the format expected by the task
        '''
        x = self._extract_input_array(problem)
        n = problem.get('n', problem.get('N', problem.get('length')))
        axis = problem.get('axis', -1)
        axis = -1 if axis is None else int(axis)
        norm = problem.get('norm', None)
        inverse = bool(problem.get('inverse', problem.get('ifft', False)))
        n_eff = self._effective_n(x, n, axis)

        if inverse:
            y = self._ifft(x, n=n, axis=axis)
        else:
            y = self._fft(x, n=n, axis=axis)

        y = self._apply_norm_scaling(y, n_eff, inverse, norm)
        return y

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
            x = self._extract_input_array(problem)
            n = problem.get('n', problem.get('N', problem.get('length')))
            axis = problem.get('axis', -1)
            axis = -1 if axis is None else int(axis)
            norm = problem.get('norm', None)
            inverse = bool(problem.get('inverse', problem.get('ifft', False)))
            n_eff = self._effective_n(x, n, axis)

            # Prefer a reference independent of SciPy: use numpy.fft
            if inverse:
                ref = np.fft.ifft(x, n=n, axis=axis)
            else:
                ref = np.fft.fft(x, n=n, axis=axis)

            ref = self._apply_norm_scaling(ref, n_eff, inverse, norm)

            # If target is provided in problem, use it as stricter reference
            target = None
            for key in ('target', 'expected', 'y'):
                if key in problem:
                    target = np.asarray(problem[key])
                    break
            if target is not None:
                ref = target

            sol = np.asarray(solution)
            if sol.shape != ref.shape:
                return False

            rtol = problem.get('rtol', None)
            atol = problem.get('atol', None)
            if rtol is None or atol is None:
                # Set tolerances based on dtype
                if np.iscomplexobj(ref) or np.iscomplexobj(sol) or ref.dtype.kind in 'fc' or sol.dtype.kind in 'fc':
                    # float64/complex128 default
                    rtol_default = 1e-7
                    atol_default = 1e-8
                    # relax for float32/complex64
                    if ref.dtype in (np.float32, np.complex64) or sol.dtype in (np.float32, np.complex64):
                        rtol_default = 1e-5
                        atol_default = 1e-6
                else:
                    rtol_default = 1e-7
                    atol_default = 1e-8
                if rtol is None:
                    rtol = rtol_default
                if atol is None:
                    atol = atol_default

            return np.allclose(sol, ref, rtol=rtol, atol=atol, equal_nan=True)
        except Exception:
            return False
