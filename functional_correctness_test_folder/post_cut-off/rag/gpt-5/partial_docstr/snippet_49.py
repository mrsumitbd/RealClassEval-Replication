class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''
    @staticmethod
    def _to_complex_array(obj):
        import numpy as np

        if obj is None:
            return None
        if isinstance(obj, dict):
            if 'real' in obj and 'imag' in obj:
                real = np.asarray(obj['real'], dtype=float)
                imag = np.asarray(obj['imag'], dtype=float)
                return real + 1j * imag
            if 'signal' in obj:
                return FFTComplexScipyFFTpack._to_complex_array(obj['signal'])
        arr = np.asarray(obj)
        if arr.dtype.kind in ('c',):
            return arr.astype(np.complex128)
        if arr.ndim == 2 and arr.shape[-1] == 2:
            return arr[..., 0].astype(float) + 1j * arr[..., 1].astype(float)
        # Try interpreting as list of pairs
        try:
            if hasattr(obj, '__iter__') and len(obj) > 0 and hasattr(obj[0], '__iter__') and len(obj[0]) == 2:
                arr = np.asarray(obj, dtype=float)
                return arr[..., 0] + 1j * arr[..., 1]
        except Exception:
            pass
        return arr.astype(np.complex128)

    @staticmethod
    def _infer_output_format(problem, input_obj):
        fmt = problem.get('output_format')
        if fmt in ('complex', 'pairs', 'separate', 'dict'):
            return fmt
        if isinstance(input_obj, dict) and ('real' in input_obj and 'imag' in input_obj):
            return 'separate'
        try:
            # list/array of pairs
            if hasattr(input_obj, '__iter__') and len(input_obj) > 0 and hasattr(input_obj[0], '__iter__') and len(input_obj[0]) == 2:
                return 'pairs'
        except Exception:
            pass
        return 'complex'

    @staticmethod
    def _format_output(y, fmt):
        import numpy as np

        y = np.asarray(y)
        if fmt == 'separate' or fmt == 'dict':
            return {'real': y.real.tolist(), 'imag': y.imag.tolist()}
        if fmt == 'pairs':
            stacked = np.stack([y.real, y.imag], axis=-1)
            return stacked.tolist()
        # default complex list
        return y.tolist()

    @staticmethod
    def _next_pow2(n):
        if n <= 1:
            return 1
        p = 1
        while p < n:
            p <<= 1
        return p

    @staticmethod
    def _compute_fft(x, n=None, axis=-1, inverse=False, norm=None, prefer_scipy=True):
        import numpy as np

        used_scipy = False
        y = None
        if prefer_scipy:
            try:
                # Try scipy.fftpack explicitly
                from scipy import fftpack as sp_fftpack  # type: ignore
                if inverse:
                    y = sp_fftpack.ifft(x, n=n, axis=axis)
                else:
                    y = sp_fftpack.fft(x, n=n, axis=axis)
                used_scipy = True
            except Exception:
                try:
                    # Modern scipy.fft
                    from scipy import fft as sp_fft  # type: ignore
                    if inverse:
                        y = sp_fft.ifft(x, n=n, axis=axis, norm=norm)
                    else:
                        y = sp_fft.fft(x, n=n, axis=axis, norm=norm)
                    used_scipy = True
                except Exception:
                    used_scipy = False

        if y is None:
            # Fallback to numpy
            import numpy.fft as npfft
            if inverse:
                y = npfft.ifft(x, n=n, axis=axis, norm=norm)
            else:
                y = npfft.fft(x, n=n, axis=axis, norm=norm)

        # Apply normalization manually if using fftpack (no norm param support)
        if used_scipy:
            # If used scipy.fftpack (no norm) we need to detect and scale; if used scipy.fft with norm, it's already applied.
            # We cannot perfectly detect which one was used above; scale only if norm in ('ortho','forward') and fftpack path likely used.
            # Heuristic: scipy.fftpack.fft/ifft do not accept norm, so y computed above without norm scaling.
            if norm in ('ortho', 'forward'):
                # Determine effective transform length per axis
                # If n provided use it, else use input length along axis
                if n is None:
                    N = x.shape[axis]
                else:
                    N = int(n)
                if N == 0:
                    return y
                if norm == 'ortho':
                    scale = 1.0 / (N ** 0.5)
                    y = y * scale
                elif norm == 'forward':
                    if not inverse:
                        y = y / N
                    # inverse remains unscaled (fftpack already applies 1/N on ifft)
        return y

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

        # Extract input
        signal = None
        for key in ('signal', 'input', 'x', 'data'):
            if key in problem:
                signal = problem[key]
                break
        if signal is None and ('real' in problem and 'imag' in problem):
            signal = {'real': problem['real'], 'imag': problem['imag']}
        if signal is None and isinstance(problem.get('signal'), dict) and ('real' in problem['signal'] and 'imag' in problem['signal']):
            signal = problem['signal']
        if signal is None:
            signal = []

        x = FFTComplexScipyFFTpack._to_complex_array(signal)

        # Optional zero padding
        n = problem.get('n', None)
        if n is None:
            if problem.get('next_pow2') or problem.get('pad_to_pow2'):
                n = FFTComplexScipyFFTpack._next_pow2(len(x))
            elif 'zero_pad_to' in problem:
                n = int(problem['zero_pad_to'])

        axis = problem.get('axis', -1)
        inverse = bool(problem.get('inverse') or problem.get(
            'ifft') or (problem.get('transform') in ('ifft', 'inverse')))
        norm = problem.get('norm', None)
        prefer_scipy = not bool(problem.get('use_numpy_only'))

        # Optional input shift
        if problem.get('fftshift_in'):
            try:
                import numpy as np
                from numpy.fft import fftshift
                x = fftshift(x, axes=axis)
            except Exception:
                pass

        y = FFTComplexScipyFFTpack._compute_fft(
            x, n=n, axis=axis, inverse=inverse, norm=norm, prefer_scipy=prefer_scipy)

        # Optional output shift
        if problem.get('fftshift') or problem.get('fftshift_out'):
            try:
                from numpy.fft import fftshift
                y = fftshift(y, axes=axis)
            except Exception:
                pass

        fmt = FFTComplexScipyFFTpack._infer_output_format(problem, signal)
        return FFTComplexScipyFFTpack._format_output(y, fmt)

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

        expected = None
        for key in ('expected', 'solution', 'output', 'y', 'result', 'answer', 'target', 'ground_truth'):
            if key in problem:
                expected = problem[key]
                break

        # If no expected provided, verify internal consistency against recomputed result
        if expected is None:
            try:
                recomputed = FFTComplexScipyFFTpack.solve(problem)
                expected = recomputed
            except Exception:
                return False

        def to_arr(obj):
            try:
                return FFTComplexScipyFFTpack._to_complex_array(obj)
            except Exception:
                return None

        a = to_arr(expected)
        b = to_arr(solution)

        if a is None or b is None:
            return False

        try:
            a = np.asarray(a).ravel()
            b = np.asarray(b).ravel()
            if a.size != b.size:
                return False
            rtol = float(problem.get('rtol', 1e-6))
            atol = float(problem.get('atol', 1e-8))
            return np.allclose(a, b, rtol=rtol, atol=atol, equal_nan=False)
        except Exception:
            return False
