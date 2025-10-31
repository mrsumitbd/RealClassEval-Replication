class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTComplexScipyFFTpack.'''
        # Try to use scipy.fftpack first; fallback to numpy.fft if unavailable
        self._use_scipy = False
        self._fft = None
        self._ifft = None
        try:
            from scipy.fftpack import fft as sp_fft, ifft as sp_ifft
            self._fft = sp_fft
            self._ifft = sp_ifft
            self._use_scipy = True
        except Exception:
            import numpy as np
            self._fft = np.fft.fft
            self._ifft = np.fft.ifft
            self._use_scipy = False

    def solve(self, problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
        Returns:
            The solution in the format expected by the task
        '''
        import numpy as np

        if not isinstance(problem, dict):
            raise TypeError("problem must be a dict")

        # Accept several common keys for input data
        for key in ("x", "input", "signal", "data"):
            if key in problem:
                x = problem[key]
                break
        else:
            raise KeyError(
                "Problem dict must contain 'x' or 'input' or 'signal' or 'data'")

        # Parameters
        inverse = bool(problem.get("inverse", False))
        n = problem.get("n", None)
        axis = problem.get("axis", -1)
        norm = problem.get("norm", None)

        x_arr = np.asarray(x)
        # Ensure complex dtype for generality
        if not np.iscomplexobj(x_arr):
            x_arr = x_arr.astype(np.complex128)
        else:
            x_arr = x_arr.astype(np.complex128, copy=False)

        # Compute effective length along axis for scaling if needed
        if n is None:
            n_eff = x_arr.shape[axis]
        else:
            n_eff = int(n)

        # Compute FFT/IFFT
        if inverse:
            if self._use_scipy:
                y = self._ifft(x_arr, n=n, axis=axis)
                if norm == "ortho":
                    # scipy ifft returns 1/n scaling; convert to 1/sqrt(n)
                    y = y * np.sqrt(n_eff)
            else:
                # numpy backend supports norm parameter directly
                y = self._ifft(x_arr, n=n, axis=axis, norm=norm)
        else:
            if self._use_scipy:
                y = self._fft(x_arr, n=n, axis=axis)
                if norm == "ortho":
                    # scipy fft is unnormalized; apply 1/sqrt(n)
                    y = y / np.sqrt(n_eff)
            else:
                y = self._fft(x_arr, n=n, axis=axis, norm=norm)

        # Return as nested lists with Python complex numbers
        return np.asarray(y).tolist()

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
            expected = self.solve(problem)
        except Exception:
            return False

        try:
            sol_arr = np.asarray(solution, dtype=np.complex128)
            exp_arr = np.asarray(expected, dtype=np.complex128)
        except Exception:
            return False

        if sol_arr.shape != exp_arr.shape:
            return False

        return np.allclose(sol_arr, exp_arr, rtol=1e-7, atol=1e-9, equal_nan=True)
