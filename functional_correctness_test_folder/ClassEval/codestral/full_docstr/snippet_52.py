
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
        total = sum(sum(row) for row in testData)
        observed_agreement = sum(testData[i][i] for i in range(k)) / total
        expected_agreement = sum(
            (sum(testData[i]) * sum(testData[j][i] for j in range(k))) for i in range(k)) / (total ** 2)
        return (observed_agreement - expected_agreement) / (1 - expected_agreement)

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
        p_j = [sum(testData[i][j] for i in range(N)) / (N * n)
               for j in range(k)]
        P_i = [sum(testData[i][j] ** 2 for j in range(k)) / (n * (n - 1))
               for i in range(N)]
        P_bar = sum(P_i) / N
        P_e_bar = sum(p_j ** 2)
        return (P_bar - P_e_bar) / (1 - P_e_bar)
