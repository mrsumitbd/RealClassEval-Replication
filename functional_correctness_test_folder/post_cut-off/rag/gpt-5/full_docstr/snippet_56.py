import numpy as np


class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTComplexScipyFFTpack.'''
        self._using_scipy = False
        self._backend = None
        try:
            from scipy import fftpack as _sp_fftpack
            self._backend = _sp_fftpack
            self._using_scipy = True
        except Exception:
            # Fallback to numpy.fft when scipy.fftpack is not available
            self._backend = np.fft

    def _get_input(self, problem):
        for key in ('data', 'signal', 'input', 'x'):
            if key in problem:
                return problem[key], key
        raise ValueError(
            'Problem must contain one of the keys: data, signal, input, x')

    def _to_array(self, x, dtype=None):
        arr = np.asarray(x)
        if dtype is not None:
            arr = arr.astype(dtype, copy=False)
        return arr

    def _scale_for_norm(self, y, transform, n_eff):
        if n_eff is None:
            return y
        if transform in ('fft',):
            # default fft has no scaling, ortho needs 1/sqrt(n)
            return y / np.sqrt(n_eff)
        elif transform in ('ifft',):
            # default ifft has 1/n factor, ortho needs 1/sqrt(n) -> multiply by sqrt(n)
            return y * np.sqrt(n_eff)
        elif transform in ('fftn',):
            return y / np.sqrt(n_eff)
        elif transform in ('ifftn',):
            return y * np.sqrt(n_eff)
        return y

    def solve(self, problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
        Returns:
            The solution in the format expected by the task
        '''
        x_in, input_key = self._get_input(problem)
        input_was_list = isinstance(x_in, (list, tuple))
        dtype = problem.get('dtype', None)
        x = self._to_array(x_in, dtype)

        # Determine transform type
        transform = problem.get('transform', None)
        if transform is None:
            inverse = problem.get('inverse', False)
            direction = problem.get('direction', None)
            if isinstance(direction, str):
                direction = direction.lower()
            if inverse or direction == 'inverse' or direction == 'backward' or direction == -1:
                transform = 'ifft'
            else:
                transform = 'fft'
        else:
            transform = str(transform).lower()

        # Parameters
        axis = problem.get('axis', -1)
        n = problem.get('n', None)
        norm = problem.get('norm', None)  # supports 'ortho' emulation
        s = problem.get('shape', problem.get('s', None))
        axes = problem.get('axes', None)

        # Perform transform
        if transform == 'fft':
            y = self._backend.fft(x, n=n, axis=axis)
            n_eff = (
                n if n is not None else x.shape[axis]) if norm == 'ortho' else None
            if norm == 'ortho':
                y = self._scale_for_norm(y, 'fft', n_eff)
        elif transform == 'ifft':
            y = self._backend.ifft(x, n=n, axis=axis)
            n_eff = (
                n if n is not None else x.shape[axis]) if norm == 'ortho' else None
            if norm == 'ortho':
                y = self._scale_for_norm(y, 'ifft', n_eff)
        elif transform == 'fftn':
            # Determine effective size product for scaling if needed
            if norm == 'ortho':
                if s is not None:
                    n_prod = int(np.prod(s))
                else:
                    use_axes = axes if axes is not None else tuple(
                        range(x.ndim))
                    if not isinstance(use_axes, (list, tuple)):
                        use_axes = (use_axes,)
                    n_prod = 1
                    for ax in use_axes:
                        n_prod *= x.shape[ax]
            else:
                n_prod = None
            # Execute
            try:
                y = self._backend.fftn(x, s=s, axes=axes)
            except TypeError:
                # Some backends may not support axes; fallback to numpy.fft.fftn
                y = np.fft.fftn(x, s=s, axes=axes)
            if norm == 'ortho':
                y = self._scale_for_norm(y, 'fftn', n_prod)
        elif transform == 'ifftn':
            if norm == 'ortho':
                if s is not None:
                    n_prod = int(np.prod(s))
                else:
                    use_axes = axes if axes is not None else tuple(
                        range(x.ndim))
                    if not isinstance(use_axes, (list, tuple)):
                        use_axes = (use_axes,)
                    n_prod = 1
                    for ax in use_axes:
                        n_prod *= x.shape[ax]
            else:
                n_prod = None
            try:
                y = self._backend.ifftn(x, s=s, axes=axes)
            except TypeError:
                y = np.fft.ifftn(x, s=s, axes=axes)
            if norm == 'ortho':
                y = self._scale_for_norm(y, 'ifftn', n_prod)
        else:
            raise ValueError(f'Unknown transform type: {transform}')

        # Optional casting of output dtype
        out_dtype = problem.get('output_dtype', None)
        if out_dtype is not None:
            y = y.astype(out_dtype, copy=False)

        # Return format
        if problem.get('as_list', False) or input_was_list:
            return y.tolist()
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
        # Normalize solution
        if isinstance(solution, dict) and 'result' in solution:
            sol = solution['result']
        else:
            sol = solution

        if sol is None:
            return False

        # If expected result provided, compare numerically
        if 'expected' in problem:
            expected = np.asarray(problem['expected'])
            sol_arr = np.asarray(sol)
            if expected.shape != sol_arr.shape:
                return False
            atol = problem.get('atol', 1e-8)
            rtol = problem.get('rtol', 1e-5)
            return np.allclose(expected, sol_arr, rtol=rtol, atol=atol)

        # Optionally validate shape if requested
        if problem.get('validate_shape', False):
            x_in, _ = self._get_input(problem)
            x = np.asarray(x_in)
            transform = str(problem.get('transform', 'fft')).lower()
            axis = problem.get('axis', -1)
            n = problem.get('n', None)
            s = problem.get('shape', problem.get('s', None))
            axes = problem.get('axes', None)

            expected_shape = list(x.shape)
            if transform in ('fft', 'ifft'):
                ax = axis if axis is not None else -1
                ax = ax if ax >= 0 else x.ndim + ax
                length = n if n is not None else x.shape[ax]
                expected_shape[ax] = length
            elif transform in ('fftn', 'ifftn'):
                if s is not None:
                    if axes is None:
                        # apply to last len(s) axes
                        use_axes = tuple(range(x.ndim - len(s), x.ndim))
                    else:
                        use_axes = axes if isinstance(
                            axes, (tuple, list)) else (axes,)
                    expected_shape = list(x.shape)
                    for k, ax in enumerate(use_axes):
                        expected_shape[ax] = s[k]
                # else shape unchanged
            sol_shape = np.asarray(sol).shape
            if tuple(expected_shape) != sol_shape:
                return False

        return True
