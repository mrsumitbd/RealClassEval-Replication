
class Convolve2DFullFill:
    def __init__(self):
        pass

    def solve(self, problem):
        """
        Compute the full 2‑D convolution of two matrices A and B.

        Parameters
        ----------
        problem : dict
            Must contain keys 'A' and 'B', each mapping to a 2‑D list of numbers.
            Example:
                {
                    'A': [[1, 2], [3, 4]],
                    'B': [[0, 1], [1, 0]]
                }

        Returns
        -------
        list[list[int]]
            The full convolution result as a 2‑D list.
        """
        A = problem.get('A')
        B = problem.get('B')
        if A is None or B is None:
            raise ValueError("Problem must contain 'A' and 'B' matrices")

        m = len(A)
        n = len(A[0]) if m > 0 else 0
        p = len(B)
        q = len(B[0]) if p > 0 else 0

        out_rows = m + p - 1
        out_cols = n + q - 1
        out = [[0] * out_cols for _ in range(out_rows)]

        for i in range(out_rows):
            for j in range(out_cols):
                s = 0
                for k in range(m):
                    for l in range(n):
                        ii = i - k
                        jj = j - l
                        if 0 <= ii < p and 0 <= jj < q:
                            s += A[k][l] * B[ii][jj]
                out[i][j] = s

        return out

    def is_solution(self, problem, solution):
        """
        Verify that a proposed solution matches the expected full convolution.

        Parameters
        ----------
        problem : dict
            Must contain 'A' and 'B' matrices. May optionally contain
            'expected' which is the correct convolution result.
        solution : list[list[int]]
            The candidate solution to verify.

        Returns
        -------
        bool
            True if the solution matches the expected result, False otherwise.
        """
        expected = problem.get('expected')
        if expected is None:
            expected = self.solve(problem)
        return solution == expected
