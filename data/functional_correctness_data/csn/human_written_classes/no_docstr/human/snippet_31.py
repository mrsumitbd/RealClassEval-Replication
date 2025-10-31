class PossibleGap:
    __slots__ = ('deadline', 'updates')

    def __init__(self, deadline: float, updates: list):
        self.deadline = deadline
        self.updates = updates

    def __repr__(self):
        return f'PossibleGap(deadline={self.deadline}, update_count={len(self.updates)})'