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
        instances = MetricsCalculator2._normalize_input(data)
        rr_list = []
        for seq, gt_total in instances:
            rr = 0.0
            if gt_total > 0:
                for idx, val in enumerate(seq, start=1):
                    if val == 1:
                        rr = 1.0 / idx
                        break
            rr_list.append(rr)
        avg_rr = sum(rr_list) / len(rr_list) if rr_list else 0.0
        return avg_rr, rr_list

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
        instances = MetricsCalculator2._normalize_input(data)
        ap_list = []
        for seq, gt_total in instances:
            if gt_total <= 0:
                ap_list.append(0.0)
                continue
            num_correct = 0
            sum_precisions = 0.0
            for idx, val in enumerate(seq, start=1):
                if val == 1:
                    num_correct += 1
                    sum_precisions += num_correct / idx
            ap = sum_precisions / gt_total
            ap_list.append(ap)
        avg_ap = sum(ap_list) / len(ap_list) if ap_list else 0.0
        return avg_ap, ap_list

    @staticmethod
    def _normalize_input(data):
        """
        Normalize input into a list of (sequence, ground_truth_total) tuples.
        """
        # Single instance: ([0/1,...], gt_total)
        if (
            isinstance(data, (list, tuple))
            and len(data) == 2
            and isinstance(data[0], (list, tuple))
            and isinstance(data[1], int)
        ):
            return [(list(data[0]), int(data[1]))]

        # Multiple instances: [([..], gt), ...] or (([..], gt), ...)
        if isinstance(data, (list, tuple)) and data and isinstance(data[0], (list, tuple)):
            first = data[0]
            if (
                isinstance(first, (list, tuple))
                and len(first) == 2
                and isinstance(first[0], (list, tuple))
                and isinstance(first[1], int)
            ):
                return [(list(item[0]), int(item[1])) for item in data]

        raise ValueError(
            "Invalid input format for MetricsCalculator2. Expected ([0/1,...], gt_total) or a list of such tuples.")
