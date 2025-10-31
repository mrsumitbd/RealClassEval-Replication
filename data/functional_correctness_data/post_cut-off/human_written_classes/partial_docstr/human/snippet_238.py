class ConstantScheduler:
    """
    Linear instead of cosine decay for the main part of the cycle.
    """

    def __call__(self, n, **kwargs):
        return 1.0

    def schedule(self, n, **kwargs):
        return 1.0