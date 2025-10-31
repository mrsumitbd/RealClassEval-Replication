class _PositionSentinel:
    """
    Provides magic values for beginning/end
    """

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Position: ' + self.name