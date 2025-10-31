
class MetricsCalculator2:
    """
    The class provides to calculate Mean Reciprocal Rank (MRR) and Mean Average Precision (MAP) based on input data,
    where MRR measures the ranking quality and MAP measures the average precision.
    """

    def __init__(self):
        pass

    @staticmethod
    def mrr(data):
        """
        compute the MRR of the input data. MRR is a widely used evaluation index. It is the mean of reciprocal rank.
        :param data: the data must be a tuple, list 0,1,eg.([1,0,...],5).  In each tuple (actual result,ground truth num),
                     ground truth num is the total ground num.
                     ([1,0,...],5),
                     or list of tuple eg. [([1,0,1,...],5),([1,0,...],6),([0,0,...],5)].
        :return: if input data is list, return the recall of this list. if the input data is list of list,
                 return the average recall on all list. The second return value is a list of precision for each input.
        >>> MetricsCalculator2.mrr(([1, 0, 1, 0], 4))
        1.0, [1.0]
        >>> MetricsCalculator2.mrr([([1, 0, 1, 0], 4), ([0, 1, 0, 1], 4)])
        0.75, [1.0, 0.5]
        """
        def _reciprocal_rank(pair):
            results, _ = pair
            for idx, val in enumerate(results):
                if val == 1:
                    return 1.0 / (idx + 1)
            return 0.0

        if isinstance(data, tuple):
            rr = _reciprocal_rank(data)
            return rr, [rr]
        elif isinstance(data, list):
            rrs = [_reciprocal_rank(pair) for pair in data]
            mean_rr = sum(rrs) / len(rrs) if rrs else 0.0
            return mean_rr, rrs
        else:
            raise TypeError("Input must be a tuple or a list of tuples")

    @staticmethod
    def map(data):
        """
        compute the MAP of the input data. MAP is a widely used evaluation index. It is the mean of AP (average precision).
        :param data: the data must be a tuple, list 0,1,eg.([1,0,...],5).  In each tuple (actual result,ground truth num),
                     ground truth num is the total ground num.
                     ([1,0,...],5),
                     or list of tuple eg. [([1,0,1,...],5),([1,0,...],6),([0,0,...],5)].
        :return: if input data is list, return the recall of this list. if the input data is list of list,
                 return the average recall on all list. The second return value is a list of precision for each input.
        >>> MetricsCalculator2.map(([1, 0, 1, 0], 4))
        0.41666666666666663, [0.41666666666666663]
        >>> MetricsCalculator2.map([([1, 0, 1, 0], 4), ([0, 1, 0, 1], 4)])
        0.3333333333333333, [0.41666666666666663, 0.25]
        """
        def _average_precision(pair):
            results, denom = pair
            if denom == 0:
                return 0.0
            num_relevant = 0
            sum_precisions = 0.0
            for idx, val in enumerate(results):
                if val == 1:
                    num_relevant += 1
                    precision_at_k = num_relevant / (idx + 1)
                    sum_precisions += precision_at_k
            return sum_precisions / denom

        if isinstance(data, tuple):
            ap = _average_precision(data)
            return ap, [ap]
        elif isinstance(data, list):
            aps = [_average_precision(pair) for pair in data]
            mean_ap = sum(aps) / len(aps) if aps else 0.0
            return mean_ap, aps
        else:
            raise TypeError("Input must be a tuple or a list of tuples")
