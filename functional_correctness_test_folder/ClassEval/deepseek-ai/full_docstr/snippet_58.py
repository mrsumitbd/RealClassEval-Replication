
class MetricsCalculator2:
    """
    The class provides to calculate Mean Reciprocal Rank (MRR) and Mean Average Precision (MAP) based on input data, where MRR measures the ranking quality and MAP measures the average precision.
    """

    def __init__(self):
        pass

    @staticmethod
    def mrr(data):
        if isinstance(data, tuple):
            actual, _ = data
            for i, val in enumerate(actual, 1):
                if val == 1:
                    return 1.0 / i, [1.0 / i]
            return 0.0, [0.0]
        elif isinstance(data, list):
            mrr_list = []
            total = 0.0
            for item in data:
                actual, _ = item
                rr = 0.0
                for i, val in enumerate(actual, 1):
                    if val == 1:
                        rr = 1.0 / i
                        break
                mrr_list.append(rr)
                total += rr
            avg_mrr = total / len(data) if len(data) > 0 else 0.0
            return avg_mrr, mrr_list

    @staticmethod
    def map(data):
        def calculate_ap(actual, ground_truth_num):
            ap = 0.0
            correct = 0
            for i, val in enumerate(actual, 1):
                if val == 1:
                    correct += 1
                    ap += correct / i
            ap = ap / ground_truth_num if ground_truth_num > 0 else 0.0
            return ap

        if isinstance(data, tuple):
            actual, ground_truth_num = data
            ap = calculate_ap(actual, ground_truth_num)
            return ap, [ap]
        elif isinstance(data, list):
            ap_list = []
            total = 0.0
            for item in data:
                actual, ground_truth_num = item
                ap = calculate_ap(actual, ground_truth_num)
                ap_list.append(ap)
                total += ap
            avg_ap = total / len(data) if len(data) > 0 else 0.0
            return avg_ap, ap_list
