class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''
    @staticmethod
    def _get_array_from_problem(problem):
        for key in ('x', 'input', 'signal', 'data'):
            if key in problem:
                return problem[key]
        raise ValueError(
            "Problem must contain one of the keys: 'x', 'input', 'signal', or 'data'.")

    @staticmethod
    def _normalize_solution_obj(solution):
        if isinstance(solution, dict):
            for key in ('result', 'y', 'output', 'fft', 'data'):
                if key in solution:
                    return solution[key]
        return solution

    @staticmethod
    def _ensure_ndarray(x, dtype=None):
        import numpy as np
        arr = np.asarray(x)
        if dtype is not None:
            arr = arr.astype(dtype, copy=False)
        return arr

    @staticmethod
    def _slice_onesided(arr, axis, n_len):
        import numpy as np
        axis = axis if axis >= 0 else arr.ndim + axis
        take_len = n_len // 2 + 1
        slicer = [slice(None)] * arr.ndim
        slicer[axis] = slice(0, take_len)
        return arr[tuple(slicer)]

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
        # Prefer SciPy fftpack if available, otherwise fallback to numpy.fft
        try:
            from scipy import fftpack as sp_fftpack
            use_scipy = True
        except Exception:
            sp_fftpack = None
            use_scipy = False

        x = FFTComplexScipyFFTpack._get_array_from_problem(problem)
        x = FFTComplexScipyFFTpack._ensure_ndarray(x)
        # Ensure complex dtype for complex FFTs; keep real if already float.
        if not np.iscomplexobj(x):
            x = x.astype(np.complex128)

        n = problem.get('n', None)
        axis = problem.get('axis', -1)
        inverse = bool(problem.get('inverse', problem.get('ifft', False)))
        norm = problem.get('norm', None)
        do_shift = bool(problem.get('shift', problem.get('fftshift', False)))
        onesided = bool(problem.get('onesided', False))

        # Compute transform
        if use_scipy:
            if inverse:
                y = sp_fftpack.ifft(x, n=n, axis=axis)
            else:
                y = sp_fftpack.fft(x, n=n, axis=axis)
        else:
            # Fallback to numpy implementation
            if inverse:
                y = np.fft.ifft(x, n=n, axis=axis)
            else:
                y = np.fft.fft(x, n=n, axis=axis)

        # Apply 'ortho' normalization to mirror numpy semantics if requested
        if norm == 'ortho':
            # Determine effective length along axis
            eff_n = n if n is not None else x.shape[axis]
            if inverse:
                # default ifft already includes 1/eff_n; to get 1/sqrt(n), multiply by sqrt(n)
                y = y * np.sqrt(eff_n)
            else:
                # default fft has no normalization; multiply by 1/sqrt(n)
                y = y / np.sqrt(eff_n)

        # Truncate to one-sided spectrum if requested
        if onesided:
            eff_n = n if n is not None else x.shape[axis]
            y = FFTComplexScipyFFTpack._slice_onesided(
                y, axis=axis, n_len=eff_n)

        # Apply fftshift if requested
        if do_shift:
            y = np.fft.fftshift(y, axes=axis)

        return y

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

        # Normalize the solution input
        sol = FFTComplexScipyFFTpack._normalize_solution_obj(solution)
        sol = FFTComplexScipyFFTpack._ensure_ndarray(sol)

        # Build reference using numpy.fft (authoritative for validation)
        x = FFTComplexScipyFFTpack._get_array_from_problem(problem)
        x = FFTComplexScipyFFTpack._ensure_ndarray(x)
        if not np.iscomplexobj(x):
            x = x.astype(np.complex128)

        n = problem.get('n', None)
        axis = problem.get('axis', -1)
        inverse = bool(problem.get('inverse', problem.get('ifft', False)))
        norm = problem.get('norm', None)
        do_shift = bool(problem.get('shift', problem.get('fftshift', False)))
        onesided = bool(problem.get('onesided', False))

        if inverse:
            ref = np.fft.ifft(x, n=n, axis=axis, norm=norm)
        else:
            ref = np.fft.fft(x, n=n, axis=axis, norm=norm)

        if onesided:
            eff_n = n if n is not None else x.shape[axis]
            ref = FFTComplexScipyFFTpack._slice_onesided(
                ref, axis=axis, n_len=eff_n)

        if do_shift:
            ref = np.fft.fftshift(ref, axes=axis)

        # Shape check
        if sol.shape != ref.shape:
            return False

        # Numerical closeness check
        # Allow small tolerances due to potential implementation differences
        return np.allclose(sol, ref, rtol=1e-7, atol=1e-9)
