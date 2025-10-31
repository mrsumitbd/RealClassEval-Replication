
class MetricsCalculator2:
    """
    The class provides to calculate Mean Reciprocal Rank (MRR) and Mean Average Precision (MAP) based on input data, where MRR measures the ranking quality and MAP measures the average precision.
    """

    def __init__(self):
        pass

    @staticmethod
    def mrr(data):
        """
        compute the MRR of the input data. MRR is a widely used evaluation index. It is the mean of reciprocal rank.
        :param data: the data must be a tuple, list 0,1,eg.([1,0,...],5).  In each tuple (actual result,ground truth num),ground truth num is the total ground num.
         ([1,0,...],5),
        or list of tuple eg. [([1,0,1,...],5),([1,0,...],6),([0,0,...],5)].
        1 stands for a correct answer, 0 stands for a wrong answer.
        :return: if input data is list, return the recall of this list. if the input data is list of list, return the
        average recall on all list. The second return value is a list of precision for each input.
        >>> MetricsCalculator2.mrr(([1, 0, 1, 0], 4))
        >>> MetricsCalculator2.mrr([([1, 0, 1, 0], 4), ([0, 1, 0, 1], 4)])
        1.0, [1.0]
        0.75, [1.0, 0.5]
        """
        def _mrr_single(item):
            preds, gt_num = item
            try:
                rank = preds.index(1) + 1
                return 1.0 / rank
            except ValueError:
                return 0.0

        if isinstance(data, tuple):
            mrr_val = _mrr_single(data)
            return mrr_val, [mrr_val]
        elif isinstance(data, list):
            mrr_list = [_mrr_single(item) for item in data]
            avg_mrr = sum(mrr_list) / len(mrr_list) if mrr_list else 0.0
            return avg_mrr, mrr_list
        else:
            raise ValueError("Input data must be a tuple or a list of tuples.")

    @staticmethod
    def map(data):
        """
        compute the MAP of the input data. MAP is a widely used evaluation index. It is the mean of AP (average precision).
        :param data: the data must be a tuple, list 0,1,eg.([1,0,...],5).  In each tuple (actual result,ground truth num),ground truth num is the total ground num.
         ([1,0,...],5),
        or list of tuple eg. [([1,0,1,...],5),([1,0,...],6),([0,0,...],5)].
        1 stands for a correct answer, 0 stands for a wrong answer.
        :return: if input data is list, return the recall of this list. if the input data is list of list, return the
        average recall on all list. The second return value is a list of precision for each input.
        >>> MetricsCalculator2.map(([1, 0, 1, 0], 4))
        >>> MetricsCalculator2.map([([1, 0, 1, 0], 4), ([0, 1, 0, 1], 4)])
        0.41666666666666663, [0.41666666666666663]
        0.3333333333333333, [0.41666666666666663, 0.25]
        """
        def _ap_single(item):
            preds, gt_num = item
            num_correct = 0
            ap_sum = 0.0
            for idx, val in enumerate(preds):
                if val == 1:
                    num_correct += 1
                    ap_sum += num_correct / (idx + 1)
            if gt_num == 0:
                return 0.0
            return ap_sum / gt_num

        if isinstance(data, tuple):
            ap_val = _ap_single(data)
            return ap_val, [ap_val]
        elif isinstance(data, list):
            ap_list = [_ap_single(item) for item in data]
            avg_ap = sum(ap_list) / len(ap_list) if ap_list else 0.0
            return avg_ap, ap_list
        else:
            raise ValueError("Input data must be a tuple or a list of tuples.")
