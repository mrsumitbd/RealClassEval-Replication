
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
        # testData is a k x k confusion matrix
        # Observed agreement
        total = 0
        agree = 0
        for i in range(k):
            for j in range(k):
                total += testData[i][j]
                if i == j:
                    agree += testData[i][j]
        po = agree / total if total > 0 else 0

        # Expected agreement
        row_marginals = [sum(testData[i]) for i in range(k)]
        col_marginals = [sum(testData[j][i] for j in range(k))
                         for i in range(k)]
        pe = 0
        for i in range(k):
            pe += (row_marginals[i] * col_marginals[i])
        pe = pe / (total * total) if total > 0 else 0

        if pe == 1:
            return 0.0
        kappa = (po - pe) / (1 - pe) if (1 - pe) != 0 else 0.0
        return kappa

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
        # testData: N x k, each row sums to n
        # Step 1: Compute p_j for each category
        p = [0.0 for _ in range(k)]
        for j in range(k):
            p[j] = sum(testData[i][j] for i in range(N)) / (N * n)
        # Step 2: Compute P_i for each subject
        P = []
        for i in range(N):
            Pi = 0.0
            for j in range(k):
                Pi += testData[i][j] * (testData[i][j] - 1)
            Pi /= (n * (n - 1))
            P.append(Pi)
        Pbar = sum(P) / N
        PbarE = sum(pj * pj for pj in p)
        if PbarE == 1:
            return 0.0
        kappa = (Pbar - PbarE) / (1 - PbarE) if (1 - PbarE) != 0 else 0.0
        return kappa
