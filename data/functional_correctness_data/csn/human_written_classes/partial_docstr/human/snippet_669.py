class PortRange:
    """
    Represents a range of ports for Router policies.
    """

    def __init__(self, a, b):
        self.min = a
        self.max = b

    def __eq__(self, b):
        return b >= self.min and b <= self.max

    def __str__(self):
        return '%d-%d' % (self.min, self.max)