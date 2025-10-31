class KappaCalculator:
    """
    This is a class as KappaCalculator, supporting to calculate Cohen's and Fleiss' kappa coefficient.
    """

    @staticmethod
    def kappa(testData, k):
        """
        Calculate the cohens kappa value of a k-dimensional matrix
        :param testData: The k-dimensional matrix that needs to calculate the cohens kappa value
        :param k: int, Matrix dimension
        :return:float, the cohens kappa value of the matrix
        >>> KappaCalculator.kappa([[2, 1, 1], [1, 2, 1], [1, 1, 2]], 3)
        0.25
        """
        # Validate input dimensions if possible
        if not testData or k <= 0:
            return 0.0
        if len(testData) != k or any(len(row) != k for row in testData):
            # If dimensions don't match k, attempt to infer; else return 0.0
            inferred_k = len(testData)
            if inferred_k == 0 or any(len(row) != inferred_k for row in testData):
                return 0.0
            k = inferred_k

        # Total observations
        total = sum(sum(row) for row in testData)
        if total == 0:
            return 0.0

        # Observed agreement
        observed = sum(testData[i][i] for i in range(k)) / float(total)

        # Expected agreement: sum over categories of (row_marginal * col_marginal) / total^2
        row_marginals = [sum(testData[i]) for i in range(k)]
        col_marginals = [sum(testData[i][j] for i in range(k))
                         for j in range(k)]
        expected = sum((row_marginals[i] * col_marginals[i])
                       for i in range(k)) / float(total * total)

        denom = 1.0 - expected
        if denom == 0.0:
            return 0.0
        return (observed - expected) / denom

    @staticmethod
    def fleiss_kappa(testData, N, k, n):
        """
        Calculate the fliss kappa value of an N * k matrix
        :param testData: Input data matrix, N * k
        :param N: int, Number of samples
        :param k: int, Number of categories
        :param n: int, Number of raters
        :return: float, fleiss kappa value
        >>> KappaCalculator.fleiss_kappa([[0, 0, 0, 0, 14],
        >>>                              [0, 2, 6, 4, 2],
        >>>                              [0, 0, 3, 5, 6],
        >>>                              [0, 3, 9, 2, 0],
        >>>                              [2, 2, 8, 1, 1],
        >>>                              [7, 7, 0, 0, 0],
        >>>                              [3, 2, 6, 3, 0],
        >>>                              [2, 5, 3, 2, 2],
        >>>                              [6, 5, 2, 1, 0],
        >>>                              [0, 2, 2, 3, 7]], 10, 5, 14)
        0.20993070442195522
        """
        # Basic validations
        if not testData or N <= 0 or k <= 0 or n <= 0:
            return 0.0
        if len(testData) != N or any(len(row) != k for row in testData):
            # Try to infer N and k from data
            N = len(testData)
            if N == 0:
                return 0.0
            k_infer = len(testData[0])
            if any(len(row) != k_infer for row in testData):
                return 0.0
            k = k_infer

        # Ensure each row sums to n; if not, proceed but avoid division by zero
        row_sums = [sum(row) for row in testData]
        if any(rs == 0 for rs in row_sums):
            return 0.0

        # Proportions per category across all subjects
        total_ratings = float(N * n)
        p_j = [sum(testData[i][j] for i in range(N)) /
               total_ratings for j in range(k)]

        # Agreement per subject
        denom_pi = float(n * (n - 1))
        if denom_pi == 0.0:
            return 0.0
        P_i = []
        for i in range(N):
            s = sum(testData[i][j] * (testData[i][j] - 1) for j in range(k))
            P_i.append(s / denom_pi)

        P_bar = sum(P_i) / float(N)
        P_e_bar = sum(p * p for p in p_j)

        denom = 1.0 - P_e_bar
        if denom == 0.0:
            return 0.0
        return (P_bar - P_e_bar) / denom
