
class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the Convolve2DFullFill.'''
        pass

    def solve(self, problem):
        """
        Compute the full 2D convolution of two input matrices.

        Parameters
        ----------
        problem : dict
            A dictionary containing two keys:
                - 'A': list of lists (m x n) matrix
                - 'B': list of lists (p x q) matrix

        Returns
        -------
        list of lists
            The full convolution result of shape (m+p-1) x (n+q-1).
        """
        A = problem.get('A')
        B = problem.get('B')

        if A is None or B is None:
            raise ValueError("Problem must contain 'A' and 'B' matrices.")

        # Convert to list of lists if not already
        A = [list(row) for row in A]
        B = [list(row) for row in B]

        m, n = len(A), len(A[0]) if A else 0
        p, q = len(B), len(B[0]) if B else 0

        # Result dimensions
        out_rows = m + p - 1
        out_cols = n + q - 1

        # Initialize output with zeros
        result = [[0 for _ in range(out_cols)] for _ in range(out_rows)]

        # Perform convolution
        for i in range(out_rows):
            for j in range(out_cols):
                acc = 0
                # Sum over all valid indices of A and B
                for ai in range(m):
                    bi = i - ai
                    if bi < 0 or bi >= p:
                        continue
                    for aj in range(n):
                        bj = j - aj
                        if bj < 0 or bj >= q:
                            continue
                        acc += A[ai][aj] * B[bi][bj]
                result[i][j] = acc

        return result

    def is_solution(self, problem, solution):
        """
        Validate that the provided solution matches the expected full convolution.

        Parameters
        ----------
        problem : dict
            The original problem dictionary containing 'A' and 'B'.
        solution : list of lists
            The proposed solution matrix.

        Returns
        -------
        bool
            True if the solution is correct, False otherwise.
        """
        try:
            expected = self.solve(problem)
        except Exception:
            return False

        # Compare shapes
        if len(solution) != len(expected):
            return False
        for row_s, row_e in zip(solution, expected):
            if len(row_s) != len(row_e):
                return False
            for val_s, val_e in zip(row_s, row_e):
                # Allow small floating point tolerance
                if isinstance(val_s, float) or isinstance(val_e, float):
                    if abs(val_s - val_e) > 1e-6:
                        return False
                else:
                    if val_s != val_e:
                        return False
        return True
