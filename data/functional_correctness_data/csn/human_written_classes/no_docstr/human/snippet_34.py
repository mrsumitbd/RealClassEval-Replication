class State:
    __slots__ = ('pts', 'deadline')

    def __init__(self, pts: int, deadline: float):
        self.pts = pts
        self.deadline = deadline

    def __repr__(self):
        return f'State(pts={self.pts}, deadline={self.deadline})'