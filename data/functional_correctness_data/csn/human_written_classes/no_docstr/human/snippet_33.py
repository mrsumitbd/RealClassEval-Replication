class Sentinel:
    __slots__ = ('tag',)

    def __init__(self, tag=None):
        self.tag = tag or '_'

    def __repr__(self):
        return self.tag