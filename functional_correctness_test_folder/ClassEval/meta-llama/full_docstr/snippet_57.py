
class MetricsCalculator:
    """
    The class calculates precision, recall, F1 score, and accuracy based on predicted and true labels.
    """

    def __init__(self):
        """
        Initialize the number of all four samples to 0
        """
        self.true_positives = 0
        self.false_positives = 0
        self.false_negatives = 0
        self.true_negatives = 0

    def update(self, predicted_labels, true_labels):
        """
        Update the number of all four samples(true_positives, false_positives, false_negatives, true_negatives)
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: None, change the number of corresponding samples
        >>> mc = MetricsCalculator()
        >>> mc.update([1, 1, 0, 0], [1, 0, 0, 1])
        (self.true_positives, self.false_positives, self.false_negatives, self.true_negatives) = (1, 1, 1, 1)
        """
        for predicted, true in zip(predicted_labels, true_labels):
            if predicted == 1 and true == 1:
                self.true_positives += 1
            elif predicted == 1 and true == 0:
                self.false_positives += 1
            elif predicted == 0 and true == 1:
                self.false_negatives += 1
            else:
                self.true_negatives += 1

    def precision(self, predicted_labels=None, true_labels=None):
        """
        Calculate precision
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        >>> mc = MetricsCalculator()
        >>> mc.update([1, 1, 0, 0], [1, 0, 0, 1])
        >>> mc.precision()
        0.5
        """
        if predicted_labels is not None and true_labels is not None:
            true_positives = sum(1 for predicted, true in zip(
                predicted_labels, true_labels) if predicted == 1 and true == 1)
            false_positives = sum(1 for predicted, true in zip(
                predicted_labels, true_labels) if predicted == 1 and true == 0)
            return true_positives / (true_positives + false_positives) if (true_positives + false_positives) != 0 else 0
        else:
            return self.true_positives / (self.true_positives + self.false_positives) if (self.true_positives + self.false_positives) != 0 else 0

    def recall(self, predicted_labels=None, true_labels=None):
        """
        Calculate recall
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        >>> mc = MetricsCalculator()
        >>> mc.update([1, 1, 0, 0], [1, 0, 0, 1])
        >>> mc.recall()
        0.5
        """
        if predicted_labels is not None and true_labels is not None:
            true_positives = sum(1 for predicted, true in zip(
                predicted_labels, true_labels) if predicted == 1 and true == 1)
            false_negatives = sum(1 for predicted, true in zip(
                predicted_labels, true_labels) if predicted == 0 and true == 1)
            return true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) != 0 else 0
        else:
            return self.true_positives / (self.true_positives + self.false_negatives) if (self.true_positives + self.false_negatives) != 0 else 0

    def f1_score(self, predicted_labels=None, true_labels=None):
        """
        Calculate f1 score, which is the harmonic mean of precision and recall
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        >>> mc = MetricsCalculator()
        >>> mc.update([1, 1, 0, 0], [1, 0, 0, 1])
        >>> mc.f1_score()
        0.5
        """
        precision = self.precision(predicted_labels, true_labels)
        recall = self.recall(predicted_labels, true_labels)
        return 2 * precision * recall / (precision + recall) if (precision + recall) != 0 else 0

    def accuracy(self, predicted_labels=None, true_labels=None):
        """
        Calculate accuracy
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        >>> mc = MetricsCalculator()
        >>> mc.update([1, 1, 0, 0], [1, 0, 0, 1])
        >>> mc.accuracy()
        0.5
        """
        if predicted_labels is not None and true_labels is not None:
            correct = sum(1 for predicted, true in zip(
                predicted_labels, true_labels) if predicted == true)
            total = len(true_labels)
            return correct / total
        else:
            total = self.true_positives + self.false_positives + \
                self.false_negatives + self.true_negatives
            return (self.true_positives + self.true_negatives) / total if total != 0 else 0
