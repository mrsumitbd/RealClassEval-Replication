from collections import defaultdict, deque

class ContextModeKeeper:
    """For computing the literal context mode.
    You feed it characters, and it computes indices in the context map.
    """

    def __init__(self, mode):
        self.chars = deque([0, 0], maxlen=2)
        self.mode = mode

    def setContextMode(self, mode):
        """Switch to given context mode (0..3)"""
        self.mode = mode

    def getIndex(self):
        if self.mode == 0:
            return self.chars[1] & 63
        elif self.mode == 1:
            return self.chars[1] >> 2
        elif self.mode == 2:
            p2, p1 = self.chars
            return self.lut0[p1] | self.lut1[p2]
        elif self.mode == 3:
            p2, p1 = self.chars
            return self.lut2[p1] << 3 | self.lut2[p2]

    def add(self, index):
        """Adjust the context for output char (as int)."""
        self.chars.append(index)
    lut0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 12, 16, 12, 12, 20, 12, 16, 24, 28, 12, 12, 32, 12, 36, 12, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 32, 32, 24, 40, 28, 12, 12, 48, 52, 52, 52, 48, 52, 52, 52, 48, 52, 52, 52, 52, 52, 48, 52, 52, 52, 52, 52, 48, 52, 52, 52, 52, 52, 24, 12, 28, 12, 12, 12, 56, 60, 60, 60, 56, 60, 60, 60, 56, 60, 60, 60, 60, 60, 56, 60, 60, 60, 60, 60, 56, 60, 60, 60, 60, 60, 24, 12, 28, 12, 0] + [0, 1] * 32 + [2, 3] * 32
    lut1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 0] + [0] * 96 + [2] * 32
    lut2 = [0] + [1] * 15 + [2] * 48 + [3] * 64 + [4] * 64 + [5] * 48 + [6] * 15 + [7]
    assert len(lut0) == len(lut1) == len(lut2) == 256