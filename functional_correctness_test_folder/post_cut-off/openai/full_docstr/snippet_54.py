
class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the Convolve2DFullFill.'''
        pass

    def _convolve(self, A, B):
        """Compute full 2‑D convolution of A and B."""
        m, n = len(A), len(A[0]) if A else 0
        p, q = len(B), len(B[0]) if B else 0
        out_rows, out_cols = m + p - 1, n + q - 1
        out = [[0.0 for _ in range(out_cols)] for _ in range(out_rows)]

        for i in range(out_rows):
            for j in range(out_cols):
                s = 0.0
                # iterate over A
                for k in range(m):
                    for l in range(n):
                        ii = i - k
                        jj = j - l
                        if 0 <= ii < p and 0 <= jj < q:
                            s += A[k][l] * B[ii][jj]
                out[i][j] = s
        return out

    def solve(self, problem):
        '''
        Solve the convolve2d_full_fill problem.
        Args:
            problem: Dictionary containing problem data specific to convolve2d_full_fill
        Returns:
            The solution in the format expected by the task
        '''
        A = problem.get('A')
        B = problem.get('B')
        if A is None or B is None:
            raise ValueError("Problem must contain 'A' and 'B' matrices.")
        return self._convolve(A, B)

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
        if not isinstance(solution, list):
            return False
        if len(solution) != len(expected):
            return False
        for row_s, row_e in zip(solution, expected):
            if len(row_s) != len(row_e):
                return False
            for val_s, val_e in zip(row_s, row_e):
                if isinstance(val_e, float):
                    if abs(val_s - val_e) > 1e-6:
                        return False
                else:
                    if val_s != val_e:
                        return False
        return True
