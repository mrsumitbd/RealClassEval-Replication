
class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the Convolve2DFullFill.'''
        pass

    @staticmethod
    def _to_matrix(x):
        if x is None:
            return None
        if isinstance(x, list):
            if not x:
                return []
            if all(isinstance(r, list) for r in x):
                return x
            return [list(x)]
        raise TypeError("Matrix must be a list of lists")

    @staticmethod
    def _flip_kernel(k):
        return [row[::-1] for row in k[::-1]]

    @staticmethod
    def _conv2d_full(a, k, do_flip=True):
        if do_flip:
            k = Convolve2DFullFill._flip_kernel(k)

        n = len(a)
        m = len(a[0]) if n > 0 else 0
        h = len(k)
        w = len(k[0]) if h > 0 else 0

        out_h = max(0, n + h - 1)
        out_w = max(0, m + w - 1)

        out = [[0 for _ in range(out_w)] for _ in range(out_h)]
        for i in range(out_h):
            for j in range(out_w):
                s = 0
                # Overlap ranges
                ai0 = max(0, i - h + 1)
                ai1 = min(n - 1, i)
                aj0 = max(0, j - w + 1)
                aj1 = min(m - 1, j)
                for ai in range(ai0, ai1 + 1):
                    ki = i - ai
                    for aj in range(aj0, aj1 + 1):
                        kj = j - aj
                        s += a[ai][aj] * k[ki][kj]
                out[i][j] = s
        return out

    @staticmethod
    def _infer_inputs(problem):
        a = None
        k = None

        # Try common keys
        if isinstance(problem, dict):
            # Primary expected keys
            a = problem.get('input', problem.get(
                'matrix', problem.get('grid', problem.get('a'))))
            k = problem.get('kernel', problem.get('filter', problem.get('k')))

        a = Convolve2DFullFill._to_matrix(a) if a is not None else None
        k = Convolve2DFullFill._to_matrix(k) if k is not None else None

        # Normalize to ints
        def normalize(mat):
            if mat is None:
                return None
            res = []
            for row in mat:
                res.append([int(v) for v in row])
            return res

        return normalize(a), normalize(k)

    def solve(self, problem):
        '''
        Solve the convolve2d_full_fill problem.
        Args:
            problem: Dictionary containing problem data specific to convolve2d_full_fill
        Returns:
            The solution in the format expected by the task
        '''
        a, k = self._infer_inputs(problem)
        if a is None or k is None:
            return None

        mode = problem.get('mode', 'full')
        if mode != 'full':
            # Task is defined for full convolution; enforce full
            mode = 'full'

        op = problem.get('operation', problem.get('op', 'convolve')).lower()
        do_flip = True if op == 'convolve' else False  # correlate if not convolve

        return self._conv2d_full(a, k, do_flip=do_flip)

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        expected = self.solve(problem)
        if expected is None or solution is None:
            return False

        # Normalize provided solution
        sol = self._to_matrix(solution)
        if sol is None:
            return False
        try:
            sol = [[int(v) for v in row] for row in sol]
        except Exception:
            return False

        if len(expected) != len(sol):
            return False
        for r1, r2 in zip(expected, sol):
            if len(r1) != len(r2):
                return False
            if any(x != y for x, y in zip(r1, r2)):
                return False
        return True
