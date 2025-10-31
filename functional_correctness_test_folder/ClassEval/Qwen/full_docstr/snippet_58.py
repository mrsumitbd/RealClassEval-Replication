
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
        """
        if not isinstance(data, list):
            data = [data]

        mrr_values = []
        for result, ground_truth_num in data:
            for rank, value in enumerate(result):
                if value == 1:
                    mrr_values.append(1 / (rank + 1))
                    break
            else:
                mrr_values.append(0)

        return sum(mrr_values) / len(mrr_values), mrr_values

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
        """
        if not isinstance(data, list):
            data = [data]

        map_values = []
        for result, ground_truth_num in data:
            relevant_items = sum(result)
            precision_sum = 0
            relevant_count = 0
            for rank, value in enumerate(result):
                if value == 1:
                    relevant_count += 1
                    precision_sum += relevant_count / (rank + 1)
            if relevant_items > 0:
                map_values.append(precision_sum / relevant_items)
            else:
                map_values.append(0)

        return sum(map_values) / len(map_values), map_values
