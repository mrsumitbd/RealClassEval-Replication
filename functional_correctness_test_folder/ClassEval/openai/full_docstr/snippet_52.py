
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
        # total number of ratings
        total = sum(sum(row) for row in testData)
        if total == 0:
            return 0.0

        # observed agreement
        observed = sum(testData[i][i] for i in range(k)) / total

        # row and column sums
        row_sums = [sum(row) for row in testData]
        col_sums = [sum(testData[i][j] for i in range(k)) for j in range(k)]

        # expected agreement
        expected = sum(row_sums[i] * col_sums[i]
                       for i in range(k)) / (total * total)

        if 1 - expected == 0:
            return 0.0
        return (observed - expected) / (1 - expected)

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
        ...                              [0, 2, 6, 4, 2],
        ...                              [0, 0, 3, 5, 6],
        ...                              [0, 3, 9, 2, 0],
        ...                              [2, 2, 8, 1, 1],
        ...                              [7, 7, 0, 0, 0],
        ...                              [3, 2, 6, 3, 0],
        ...                              [2, 5, 3, 2, 2],
        ...                              [6, 5, 2, 1, 0],
        ...                              [0, 2, 2, 3, 7]], 10, 5, 14)
        0.20993070442195522
        """
        if N == 0 or n <= 1:
            return 0.0

        # Compute Pi for each item
        Pi = []
        for i in range(N):
            sum_ij = sum(testData[i][j] * (testData[i][j] - 1)
                         for j in range(k))
            Pi.append(sum_ij / (n * (n - 1)))

        P_bar = sum(Pi) / N

        # Compute p_j for each category
        p_j = []
        for j in range(k):
            col_sum = sum(testData[i][j] for i in range(N))
            p_j.append(col_sum / (N * n))

        Pe = sum(p * p for p in p_j)

        if 1 - Pe == 0:
            return 0.0
        return (P_bar - Pe) / (1 - Pe)
