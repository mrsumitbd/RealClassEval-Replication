import numpy as np


class FFTConvolution:
    '''
    Initial implementation of fft_convolution task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTConvolution.'''
        self._rtol = 1e-6
        self._atol = 1e-8

    def _extract_arrays_from_problem(self, problem):
        candidates = [
            ('a', 'b'),
            ('signal', 'kernel'),
            ('x', 'h'),
            ('poly1', 'poly2'),
        ]
        a = b = None
        for k1, k2 in candidates:
            if k1 in problem and k2 in problem:
                a = problem[k1]
                b = problem[k2]
                break
        if a is None or b is None:
            raise ValueError(
                "Problem must contain two arrays: e.g., ('a','b') or ('signal','kernel').")
        a = np.asarray(a)
        b = np.asarray(b)
        return a, b

    def _fft_convolve_nd(self, a: np.ndarray, b: np.ndarray, mode: str = 'full'):
        mode = (mode or 'full').lower()
        if a.ndim != b.ndim:
            raise ValueError(
                "Input arrays must have the same number of dimensions.")

        # Determine output shape
        if mode in ('circular', 'wrap'):
            s = a.shape
        else:
            s = tuple(int(da + db - 1) for da, db in zip(a.shape, b.shape))

        # Choose real vs complex FFT path
        use_real = not (np.iscomplexobj(a) or np.iscomplexobj(b))

        if use_real:
            Fa = np.fft.rfftn(a, s=s)
            Fb = np.fft.rfftn(b, s=s)
            Fc = Fa * Fb
            full = np.fft.irfftn(Fc, s=s)
        else:
            Fa = np.fft.fftn(a, s=s)
            Fb = np.fft.fftn(b, s=s)
            Fc = Fa * Fb
            full = np.fft.ifftn(Fc, s=s)

        full = np.real_if_close(full, tol=1000)

        if mode in ('circular', 'wrap'):
            return full

        # Cropping for 'same' and 'valid'
        a_shape = np.array(a.shape, dtype=int)
        b_shape = np.array(b.shape, dtype=int)

        if mode == 'full':
            return full

        if mode == 'same':
            starts = ((b_shape - 1) // 2).astype(int)
            ends = starts + a_shape
            slices = tuple(slice(int(st), int(en))
                           for st, en in zip(starts, ends))
            return full[slices]

        if mode == 'valid':
            out_shape = a_shape - b_shape + 1
            if np.any(out_shape <= 0):
                # Return empty array with correct number of dims
                return np.zeros(tuple(max(int(x), 0) for x in out_shape), dtype=full.dtype)
            starts = (b_shape - 1).astype(int)
            ends = starts + out_shape
            slices = tuple(slice(int(st), int(en))
                           for st, en in zip(starts, ends))
            return full[slices]

        raise ValueError(f"Unsupported mode: {mode}")

    def solve(self, problem):
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
        Returns:
            The solution in the format expected by the task
        '''
        a, b = self._extract_arrays_from_problem(problem)
        mode = problem.get('mode', 'full')

        if problem.get('circular', False):
            mode = 'circular'

        result = self._fft_convolve_nd(a, b, mode=mode)

        # If both inputs were integer types and the result is close to integers, optionally round
        if np.issubdtype(np.asarray(a).dtype, np.integer) and np.issubdtype(np.asarray(b).dtype, np.integer):
            rounded = np.rint(result)
            if np.allclose(result, rounded, rtol=self._rtol, atol=self._atol):
                result = rounded.astype(np.int64)

        return result.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Normalize provided solution
        sol = solution
        if isinstance(solution, dict):
            for key in ('result', 'convolution', 'y', 'output'):
                if key in solution:
                    sol = solution[key]
                    break
        sol_arr = np.asarray(sol)

        # Compute expected
        expected = np.asarray(self.solve(problem))

        if sol_arr.shape != expected.shape:
            return False

        # Exact compare if integers, otherwise allclose
        if np.issubdtype(sol_arr.dtype, np.integer) and np.issubdtype(expected.dtype, np.integer):
            return np.array_equal(sol_arr, expected)
        return np.allclose(sol_arr, expected, rtol=self._rtol, atol=self._atol)
