
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

        Returns
        -------
        list[list[float]]
            The convolution result as a 2‑D list.
        """
        A = problem.get('A')
        B = problem.get('B')
        if A is None or B is None:
            raise ValueError("Problem must contain 'A' and 'B' matrices")

        # Dimensions
        hA, wA = len(A), len(A[0]) if A else 0
        hB, wB = len(B), len(B[0]) if B else 0

        # Result dimensions
        hR, wR = hA + hB - 1, wA + wB - 1
        result = [[0.0 for _ in range(wR)] for _ in range(hR)]

        # Full convolution
        for i in range(hA):
            for j in range(wA):
                a_val = A[i][j]
                for k in range(hB):
                    for l in range(wB):
                        result[i + k][j + l] += a_val * B[k][l]
        return result

    def is_solution(self, problem, solution):
        """
        Verify that the provided solution is the correct full convolution.

        Parameters
        ----------
        problem : dict
            Must contain keys 'A' and 'B'.
        solution : list[list[float]]
            The candidate solution matrix.

        Returns
        -------
        bool
            True if solution matches the convolution of A and B, False otherwise.
        """
        try:
            expected = self.solve(problem)
        except Exception:
            return False

        # Compare shapes
        if len(expected) != len(solution):
            return False
        if any(len(row) != len(solution[i]) for i, row in enumerate(expected)):
            return False

        # Compare values with tolerance for floating point
        eps = 1e-9
        for i in range(len(expected)):
            for j in range(len(expected[0])):
                if abs(expected[i][j] - solution[i][j]) > eps:
                    return False
        return True
