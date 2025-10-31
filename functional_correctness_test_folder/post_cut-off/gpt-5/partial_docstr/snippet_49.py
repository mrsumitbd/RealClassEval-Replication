class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''
    @staticmethod
    def _to_complex_array(x):
        import numpy as np
        if x is None:
            return None
        # Accept numpy array directly
        if isinstance(x, np.ndarray):
            if np.iscomplexobj(x):
                return x.astype(np.complex128, copy=False)
            # If structured as (..., 2) real/imag pairs
            if x.ndim >= 1 and x.shape[-1] == 2:
                return x[..., 0].astype(np.float64) + 1j * x[..., 1].astype(np.float64)
            # If purely real array
            return x.astype(np.float64) + 0j
        # Dict with separate real/imag
        if isinstance(x, dict):
            real = x.get('real', None)
            imag = x.get('imag', None)
            if real is None or imag is None:
                raise ValueError("Missing 'real' or 'imag' in input dict")
            real = np.asarray(real, dtype=np.float64)
            imag = np.asarray(imag, dtype=np.float64)
            return real + 1j * imag
        # List/tuple
        if isinstance(x, (list, tuple)):
            if len(x) == 0:
                return np.array([], dtype=np.complex128)
            # Check if list of pairs
            first = x[0]
            if isinstance(first, (list, tuple)) and len(first) == 2 and all(isinstance(v, (int, float)) for v in first):
                import numpy as np
                arr = np.asarray(x, dtype=np.float64)
                return arr[:, 0] + 1j * arr[:, 1]
            # If list of complex or numbers
            return np.asarray(x, dtype=np.complex128)
        # Single number
        if isinstance(x, (int, float, complex)):
            import numpy as np
            return np.asarray([x], dtype=np.complex128)
        raise TypeError("Unsupported input type for complex array conversion")

    @staticmethod
    def _from_complex_array(z, template=None):
        import numpy as np
        z = np.asarray(z, dtype=np.complex128)
        # If template hints desired format
        if isinstance(template, dict) and ('real' in template or 'imag' in template):
            return {'real': z.real.tolist(), 'imag': z.imag.tolist()}
        if isinstance(template, (list, tuple)) and len(template) > 0:
            first = template[0]
            if isinstance(first, (list, tuple)) and len(first) == 2 and all(isinstance(v, (int, float)) for v in first):
                pairs = np.stack((z.real, z.imag), axis=-1)
                return pairs.tolist()
            if isinstance(first, complex):
                return z.tolist()
            if isinstance(first, (int, float)):
                # Input was real list; still return complex as pairs to be safe
                pairs = np.stack((z.real, z.imag), axis=-1)
                return pairs.tolist()
        # Default to list of [real, imag] pairs for JSON safety
        pairs = np.stack((z.real, z.imag), axis=-1)
        return pairs.tolist()

    @staticmethod
    def _compute_fft(x, n=None):
        try:
            # Prefer scipy.fftpack if available
            from scipy.fftpack import fft as sp_fft
            return sp_fft(x, n=n)
        except Exception:
            # Fallback to numpy
            import numpy as np
            return np.fft.fft(x, n=n)

    @staticmethod
    def solve(problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
        Returns:
            The solution in the format expected by the task
        '''
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dict")
        x_in = problem.get('x', None)
        if x_in is None and 'signal' in problem:
            x_in = problem.get('signal')
        n = problem.get('n', None)
        x = FFTComplexScipyFFTpack._to_complex_array(x_in)
        y = FFTComplexScipyFFTpack._compute_fft(x, n=n)
        return FFTComplexScipyFFTpack._from_complex_array(y, template=x_in)

    @staticmethod
    def is_solution(problem, solution):
        import numpy as np
        # Build reference
        x_in = problem.get('x', None)
        if x_in is None and 'signal' in problem:
            x_in = problem.get('signal')
        n = problem.get('n', None)
        x = FFTComplexScipyFFTpack._to_complex_array(x_in)
        ref = np.fft.fft(x, n=n)

        # Normalize provided solution to complex array
        try:
            sol = FFTComplexScipyFFTpack._to_complex_array(solution)
        except Exception:
            # Try to infer from dict with expected key
            if isinstance(solution, dict) and ('real' in solution or 'imag' in solution):
                real = np.asarray(solution.get('real', []), dtype=np.float64)
                imag = np.asarray(solution.get('imag', []), dtype=np.float64)
                sol = real + 1j * imag
            else:
                return False

        if sol.shape != ref.shape:
            return False
        return np.allclose(sol, ref, rtol=1e-7, atol=1e-9)
