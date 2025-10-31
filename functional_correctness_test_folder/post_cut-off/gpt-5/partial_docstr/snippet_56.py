class FFTComplexScipyFFTpack:

    def __init__(self):
        '''Initialize the FFTComplexScipyFFTpack.'''
        self._backend = None
        self._fft = None
        self._ifft = None
        try:
            import scipy.fftpack as sp_fftpack
            self._backend = "scipy.fftpack"
            self._fft = sp_fftpack.fft
            self._ifft = sp_fftpack.ifft
        except Exception:
            import numpy.fft as np_fft
            self._backend = "numpy.fft"
            self._fft = np_fft.fft
            self._ifft = np_fft.ifft

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

        # Accept several common keys for the input signal
        x = None
        for key in ("signal", "input", "data", "x"):
            if key in problem:
                x = problem[key]
                break
        if x is None:
            raise KeyError(
                "problem must contain one of the keys: 'signal', 'input', 'data', or 'x'")

        x = np.asarray(x)
        n = problem.get("n", None)
        axis = problem.get("axis", -1)
        inverse = bool(problem.get("inverse", False))
        norm = problem.get("norm", None)  # None/backward/ortho/forward

        if inverse:
            y = self._ifft(x, n=n, axis=axis)
        else:
            y = self._fft(x, n=n, axis=axis)

        # Determine the effective length n used along the axis for scaling purposes
        if n is None:
            n_eff = x.shape[axis] if x.shape != () else 1
        else:
            n_eff = int(n) if n is not None else 1
            if n_eff <= 0:
                raise ValueError("n must be a positive integer when provided")

        # Emulate normalization modes similar to scipy.fft interface
        # fftpack/numpy.fft use backward normalization by default: forward no scale, inverse 1/n
        if norm is not None:
            if norm not in (None, "backward", "ortho", "forward"):
                raise ValueError(
                    "norm must be one of None, 'backward', 'ortho', or 'forward'")
            if norm == "forward":
                if inverse:
                    # desired: inverse with no scaling; ifft currently applies 1/n -> multiply by n
                    y = y * n_eff
                else:
                    # desired: forward with 1/n scaling
                    y = y / n_eff
            elif norm == "ortho":
                scale = np.sqrt(n_eff) if n_eff > 0 else 1.0
                if inverse:
                    # ifft currently applies 1/n, need net 1/sqrt(n) -> multiply by sqrt(n)
                    y = y * scale
                else:
                    # forward currently no scale, need 1/sqrt(n)
                    y = y / scale
            # 'backward' or None: leave as backend default

        return {
            "result": y,
            "backend": self._backend,
        }

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

        # Extract result from solution
        if isinstance(solution, dict) and "result" in solution:
            res = solution["result"]
        else:
            res = solution

        res = np.asarray(res)

        expected = self.solve(problem)["result"]

        rtol = problem.get("rtol", 1e-7)
        atol = problem.get("atol", 1e-8)

        try:
            return np.allclose(res, expected, rtol=rtol, atol=atol, equal_nan=True)
        except Exception:
            return False
