class Counter:
    """
    A counter whose instances provides an incremental value when called

    :ivar count: the next index for creation.
    """
    __slots__ = ('count',)

    def __init__(self):
        self.count = 0

    def __call__(self):
        count = self.count
        self.count += 1
        return count