import numpy as np
import inspect

try:
    import scipy.fftpack as sp_fftpack
    _SCIPY_FFTPACK_AVAILABLE = True
except Exception:
    sp_fftpack = None
    _SCIPY_FFTPACK_AVAILABLE = False


class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTComplexScipyFFTpack.'''
        self._use_scipy_fftpack = _SCIPY_FFTPACK_AVAILABLE
        if self._use_scipy_fftpack:
            self._fft_func = sp_fftpack.fft
            self._ifft_func = sp_fftpack.ifft
        else:
            self._fft_func = np.fft.fft
            self._ifft_func = np.fft.ifft
        self._fft_sig = inspect.signature(self._fft_func)
        self._ifft_sig = inspect.signature(self._ifft_func)

    def _extract_signal(self, problem):
        # Attempt to get complex signal from various common keys
        possible_keys = ['x', 'signal', 'data', 'input', 'array', 'values']
        arr = None
        for k in possible_keys:
            if k in problem:
                arr = problem[k]
                break

        # Real/imag provided separately
        if arr is None:
            # try keys directly on problem
            if 'real' in problem and 'imag' in problem:
                real = np.asarray(problem['real'])
                imag = np.asarray(problem['imag'])
                return real + 1j * imag
            if 'x_real' in problem and 'x_imag' in problem:
                real = np.asarray(problem['x_real'])
                imag = np.asarray(problem['x_imag'])
                return real + 1j * imag
            raise ValueError('No input signal found in problem.')

        # If arr itself is a dict with real/imag
        if isinstance(arr, dict):
            if 'real' in arr and 'imag' in arr:
                real = np.asarray(arr['real'])
                imag = np.asarray(arr['imag'])
                return real + 1j * imag

        # If list of [re, im] pairs
        a = np.asarray(arr)
        if a.dtype == object:
            # try to coerce
            try:
                a = np.array(arr, dtype=float)
            except Exception:
                pass
        if a.ndim >= 1 and a.shape[-1] == 2:
            # interpret as (..., 2) -> complex
            real = a[..., 0]
            imag = a[..., 1]
            return np.asanyarray(real) + 1j * np.asanyarray(imag)

        # Already complex or numeric
        a = np.asarray(arr)
        return a

    def _get_params(self, problem):
        # Determine transform direction
        inverse = False
        if 'inverse' in problem:
            inverse = bool(problem['inverse'])
        elif 'ifft' in problem:
            inverse = bool(problem['ifft'])
        elif 'direction' in problem:
            direction = str(problem['direction']).lower()
            inverse = direction in ('inverse', 'backward', 'ifft')
        elif 'op' in problem:
            op = str(problem['op']).lower()
            inverse = op in ('ifft', 'inverse')
        elif 'transform' in problem:
            t = str(problem['transform']).lower()
            inverse = t in ('ifft', 'inverse')

        # Size/axis/norm
        axis = problem.get('axis', -1)
        n = problem.get('n', None)
        if n is None:
            n = problem.get('length', None)
        norm = problem.get('norm', None)
        return inverse, n, axis, norm

    def _call_fft_like(self, func, sig, a, n, axis, norm):
        kwargs = {}
        params = sig.parameters
        if 'a' in params or 'x' in params:
            pass  # positional will cover this
        if 'n' in params and n is not None:
            kwargs['n'] = int(n)
        if 'axis' in params and axis is not None:
            kwargs['axis'] = int(axis)
        if 'norm' in params and norm is not None:
            kwargs['norm'] = norm
        # Some scipy.fftpack versions don't support norm; signature check handles it
        return func(a, **kwargs)

    def solve(self, problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
        Returns:
            The solution in the format expected by the task
        '''
        x = self._extract_signal(problem)
        inverse, n, axis, norm = self._get_params(problem)
        if inverse:
            y = self._call_fft_like(
                self._ifft_func, self._ifft_sig, x, n, axis, norm)
        else:
            y = self._call_fft_like(
                self._fft_func, self._fft_sig, x, n, axis, norm)
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
        # Normalize solution to ndarray
        sol = solution
        if isinstance(solution, dict):
            for key in ('y', 'output', 'result', 'solution'):
                if key in solution:
                    sol = solution[key]
                    break
        sol = np.asarray(sol)

        # Compare against expected if provided
        expected = None
        for key in ('expected', 'target', 'y', 'output', 'result'):
            if key in problem:
                expected = np.asarray(problem[key])
                break
        rtol = problem.get('rtol', 1e-7)
        atol = problem.get('atol', 1e-9)

        if expected is not None:
            try:
                return np.allclose(sol, expected, rtol=rtol, atol=atol, equal_nan=True)
            except Exception:
                return False

        # Otherwise, verify invertibility property with the same parameters
        try:
            x = self._extract_signal(problem)
            inverse, n, axis, norm = self._get_params(problem)
            if inverse:
                # solution = ifft(x) -> fft(solution) should recover x
                if self._use_scipy_fftpack:
                    check = sp_fftpack.fft(
                        sol, n=n if n is not None else None, axis=axis)
                else:
                    check = np.fft.fft(
                        sol, n=n if n is not None else None, axis=axis, norm=norm)
                return np.allclose(check, x, rtol=rtol, atol=atol, equal_nan=True)
            else:
                # solution = fft(x) -> ifft(solution) should recover x
                if self._use_scipy_fftpack:
                    check = sp_fftpack.ifft(
                        sol, n=n if n is not None else None, axis=axis)
                else:
                    check = np.fft.ifft(
                        sol, n=n if n is not None else None, axis=axis, norm=norm)
                return np.allclose(check, x, rtol=rtol, atol=atol, equal_nan=True)
        except Exception:
            return False
