import numpy as np


class FFTConvolution:
    '''
    Initial implementation of fft_convolution task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTConvolution.'''
        pass

    def _get_arrays(self, problem):
        # Try multiple common key pairs
        key_pairs = [
            ('a', 'b'),
            ('x', 'h'),
            ('signal', 'kernel'),
            ('input', 'filter'),
        ]
        for k1, k2 in key_pairs:
            if k1 in problem and k2 in problem:
                return np.asarray(problem[k1]), np.asarray(problem[k2])
        # If a single key 'arrays' or 'inputs' with tuple/list
        for k in ('arrays', 'inputs'):
            if k in problem:
                arrs = problem[k]
                if isinstance(arrs, (list, tuple)) and len(arrs) == 2:
                    return np.asarray(arrs[0]), np.asarray(arrs[1])
        raise ValueError(
            'Problem must contain two input arrays (e.g., a/b, x/h, signal/kernel, or input/filter).')

    def _next_pow2(self, n):
        n = int(n)
        if n <= 1:
            return 1
        return 1 << (n - 1).bit_length()

    def _pad_shape(self, shape):
        return tuple(self._next_pow2(s) for s in shape)

    def _align_dims(self, a, b):
        # Ensure same number of dimensions by prepending singleton dims
        na, nb = a.ndim, b.ndim
        if na < nb:
            a = a.reshape((1,) * (nb - na) + a.shape)
        elif nb < na:
            b = b.reshape((1,) * (na - nb) + b.shape)
        return a, b

    def _fft_convolve_full(self, a, b):
        a, b = self._align_dims(a, b)
        # Determine working dtype
        is_complex = np.iscomplexobj(a) or np.iscomplexobj(b)
        work_dtype = np.complex128 if is_complex else np.float64

        a = a.astype(work_dtype, copy=False)
        b = b.astype(work_dtype, copy=False)

        full_shape = tuple(sa + sb - 1 for sa, sb in zip(a.shape, b.shape))
        fft_shape = self._pad_shape(full_shape)

        Fa = np.fft.fftn(a, s=fft_shape)
        Fb = np.fft.fftn(b, s=fft_shape)
        conv = np.fft.ifftn(Fa * Fb)

        # Trim to full (linear) convolution size
        slices = tuple(slice(0, s) for s in full_shape)
        conv_full = conv[slices]
        if not is_complex:
            conv_full = conv_full.real
        return conv_full

    def _crop_mode(self, conv_full, a_shape, b_shape, mode):
        if mode == 'full':
            return conv_full
        if mode == 'same':
            # Centered cropping to match a_shape
            starts = [(sb - 1) // 2 for sb in b_shape]
            ends = [st + sa for st, sa in zip(starts, a_shape)]
            slices = tuple(slice(st, en) for st, en in zip(starts, ends))
            return conv_full[slices]
        if mode == 'valid':
            # Positions where kernel fully overlaps signal
            valid_shape = tuple(max(sa - sb + 1, 0)
                                for sa, sb in zip(a_shape, b_shape))
            # start index is sb - 1 along each axis
            starts = [sb - 1 for sb in b_shape]
            ends = [st + vs for st, vs in zip(starts, valid_shape)]
            # Handle empty outputs
            if any(vs <= 0 for vs in valid_shape):
                return np.empty(valid_shape, dtype=conv_full.dtype)
            slices = tuple(slice(st, en) for st, en in zip(starts, ends))
            return conv_full[slices]
        raise ValueError("mode must be one of: 'full', 'same', 'valid'")

    def solve(self, problem):
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
        Returns:
            The solution in the format expected by the task
        '''
        a, b = self._get_arrays(problem)
        mode = str(problem.get('mode', 'full')).lower()
        conv_full = self._fft_convolve_full(a, b)
        a_aligned, b_aligned = self._align_dims(np.empty_like(
            a, shape=a.shape), np.empty_like(b, shape=b.shape))
        result = self._crop_mode(
            conv_full, a_aligned.shape, b_aligned.shape, mode)
        return {'result': result.tolist()}

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
            computed = self.solve(problem)
        except Exception:
            return False

        comp_arr = np.asarray(computed.get('result'))
        if isinstance(solution, dict):
            # Try common keys
            for k in ('result', 'convolution', 'output'):
                if k in solution:
                    sol_arr = np.asarray(solution[k])
                    break
            else:
                return False
        else:
            sol_arr = np.asarray(solution)

        if comp_arr.shape != sol_arr.shape:
            return False

        return np.allclose(comp_arr, sol_arr, rtol=1e-7, atol=1e-8, equal_nan=True)
