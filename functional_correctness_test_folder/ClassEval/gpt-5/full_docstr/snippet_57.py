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

    @staticmethod
    def _validate_inputs(predicted_labels, true_labels):
        if not isinstance(predicted_labels, list) or not isinstance(true_labels, list):
            raise TypeError("predicted_labels and true_labels must be lists")
        if len(predicted_labels) != len(true_labels):
            raise ValueError(
                "predicted_labels and true_labels must have the same length")

    @staticmethod
    def _confusion_counts(predicted_labels, true_labels):
        MetricsCalculator._validate_inputs(predicted_labels, true_labels)
        tp = fp = fn = tn = 0
        for p, t in zip(predicted_labels, true_labels):
            if p == 1 and t == 1:
                tp += 1
            elif p == 1 and t == 0:
                fp += 1
            elif p == 0 and t == 1:
                fn += 1
            elif p == 0 and t == 0:
                tn += 1
            else:
                # For non-binary values, ignore or treat as mismatch
                # Here we raise an error to enforce binary labels 0/1
                raise ValueError("Labels must be binary (0 or 1)")
        return tp, fp, fn, tn

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
        tp, fp, fn, tn = self._confusion_counts(predicted_labels, true_labels)
        self.true_positives += tp
        self.false_positives += fp
        self.false_negatives += fn
        self.true_negatives += tn

    def precision(self, predicted_labels, true_labels):
        """
        Calculate precision
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        >>> mc = MetricsCalculator()
        >>> mc.precision([1, 1, 0, 0], [1, 0, 0, 1])
        0.5
        """
        tp, fp, _, _ = self._confusion_counts(predicted_labels, true_labels)
        denom = tp + fp
        return tp / denom if denom != 0 else 0.0

    def recall(self, predicted_labels, true_labels):
        """
        Calculate recall
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        >>> mc = MetricsCalculator()
        >>> mc.recall([1, 1, 0, 0], [1, 0, 0, 1])
        0.5
        """
        tp, _, fn, _ = self._confusion_counts(predicted_labels, true_labels)
        denom = tp + fn
        return tp / denom if denom != 0 else 0.0

    def f1_score(self, predicted_labels, true_labels):
        """
        Calculate f1 score, which is the harmonic mean of precision and recall
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        >>> mc = MetricsCalculator()
        >>> mc.f1_score([1, 1, 0, 0], [1, 0, 0, 1])
        0.5
        """
        p = self.precision(predicted_labels, true_labels)
        r = self.recall(predicted_labels, true_labels)
        denom = p + r
        return (2 * p * r) if denom != 0 else 0.0 if denom == 0 else (2 * p * r / denom)

    def accuracy(self, predicted_labels, true_labels):
        """
        Calculate accuracy
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        >>> mc = MetricsCalculator()
        >>>mc.accuracy([1, 1, 0, 0], [1, 0, 0, 1])
        0.5
        """
        tp, fp, fn, tn = self._confusion_counts(predicted_labels, true_labels)
        total = tp + fp + fn + tn
        return (tp + tn) / total if total != 0 else 0.0
