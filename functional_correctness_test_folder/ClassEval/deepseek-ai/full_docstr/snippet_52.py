
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
        po = sum(testData[i][i] for i in range(k)) / total
        pe = sum(sum(testData[i]) * sum(testData[j][i]
                 for j in range(k)) for i in range(k)) / (total ** 2)
        return (po - pe) / (1 - pe) if pe != 1 else 0.0

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
        pj = [0.0] * k
        for row in testData:
            for j in range(k):
                pj[j] += row[j]
        for j in range(k):
            pj[j] /= (N * n)

        sum_pj_sq = sum(pj[j] ** 2 for j in range(k))

        Pi = []
        for row in testData:
            numerator = sum(row[j] * (row[j] - 1) for j in range(k))
            Pi.append(numerator / (n * (n - 1)))

        P_avg = sum(Pi) / N
        Pe = sum_pj_sq

        return (P_avg - Pe) / (1 - Pe) if Pe != 1 else 0.0
