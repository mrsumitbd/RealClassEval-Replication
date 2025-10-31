class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the Convolve2DFullFill.'''
        pass

    def _to_2d_list(self, arr):
        if isinstance(arr, list):
            return arr
        try:
            import numpy as np
            if isinstance(arr, np.ndarray):
                return arr.tolist()
        except Exception:
            pass
        return arr

    def _to_numpy(self, grid):
        import numpy as np
        if isinstance(grid, np.ndarray):
            return grid
        return np.array(grid, dtype=int)

    def _full_convolve2d(self, a, k):
        import numpy as np
        A = self._to_numpy(a).astype(int)
        K = self._to_numpy(k).astype(int)

        Kh, Kw = K.shape
        Ah, Aw = A.shape
        # Flip kernel for convolution
        Kf = K[::-1, ::-1]

        Oh = Ah + Kh - 1
        Ow = Aw + Kw - 1
        out = np.zeros((Oh, Ow), dtype=int)

        # Offsets to align
        off_h = Kh - 1
        off_w = Kw - 1

        # Naive implementation
        for i in range(Oh):
            for j in range(Ow):
                s = 0
                # Compute dot product for this location
                for ki in range(Kh):
                    ai = i - off_h + ki
                    if ai < 0 or ai >= Ah:
                        continue
                    for kj in range(Kw):
                        aj = j - off_w + kj
                        if aj < 0 or aj >= Aw:
                            continue
                        s += Kf[ki, kj] * A[ai, aj]
                out[i, j] = s
        return out

    def solve(self, problem):
        '''
        Solve the convolve2d_full_fill problem.
        Args:
            problem: Dictionary containing problem data specific to convolve2d_full_fill
        Returns:
            The solution in the format expected by the task
        '''
        # Expected keys:
        # - input (2D array-like of ints)
        # - kernel (2D array-like of ints)
        # Optional postprocessing:
        # - threshold (int): binarize output as 1 if >= threshold else 0
        # - binary (bool): if True, any non-zero -> 1
        # - fill_value (int): if provided, any non-zero -> fill_value
        # - clip_min (int), clip_max (int): clip the output range
        if not isinstance(problem, dict):
            raise ValueError("Problem must be a dictionary")

        grid = problem.get('input')
        kernel = problem.get('kernel')
        if grid is None or kernel is None:
            raise ValueError("Problem must contain 'input' and 'kernel'")

        conv = self._full_convolve2d(grid, kernel)

        # Post-processing
        threshold = problem.get('threshold', None)
        binary = problem.get('binary', False)
        fill_value = problem.get('fill_value', None)
        clip_min = problem.get('clip_min', None)
        clip_max = problem.get('clip_max', None)

        if threshold is not None:
            conv = (conv >= int(threshold)).astype(int)

        if binary:
            conv = (conv != 0).astype(int)

        if fill_value is not None:
            fv = int(fill_value)
            conv = (conv != 0).astype(int) * fv

        if clip_min is not None or clip_max is not None:
            import numpy as np
            lo = -np.inf if clip_min is None else int(clip_min)
            hi = np.inf if clip_max is None else int(clip_max)
            conv = conv.clip(lo, hi)

        return self._to_2d_list(conv)

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Validation approach:
        # - If problem has 'expected'/'target'/'output', compare exact equality.
        # - Else, verify solution is a 2D list of ints matching expected shape (if provided).
        # - If no target and no expected shape, ensure solution is well-formed 2D list of ints.
        import numpy as np

        def is_2d_int_list(x):
            if not isinstance(x, list) or len(x) == 0:
                return False
            row_len = None
            for row in x:
                if not isinstance(row, list) or len(row) == 0:
                    return False
                if row_len is None:
                    row_len = len(row)
                elif row_len != len(row):
                    return False
                for v in row:
                    if not isinstance(v, (int, np.integer)):
                        return False
            return True

        sol = solution
        if isinstance(solution, dict) and 'output' in solution:
            sol = solution['output']

        if not is_2d_int_list(sol):
            return False

        target = None
        for key in ('expected', 'target', 'output'):
            if isinstance(problem.get(key), list):
                target = problem.get(key)
                break

        if target is not None:
            try:
                return np.array_equal(np.array(sol, dtype=int), np.array(target, dtype=int))
            except Exception:
                return sol == target

        # If expected shape is provided
        expected_shape = problem.get('expected_shape')
        if expected_shape is not None and isinstance(expected_shape, (list, tuple)) and len(expected_shape) == 2:
            try:
                arr = np.array(sol, dtype=int)
                return tuple(arr.shape) == (int(expected_shape[0]), int(expected_shape[1]))
            except Exception:
                return False

        return True
