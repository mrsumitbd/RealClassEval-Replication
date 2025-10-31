class Token:
    """A token representation used for token clustering."""

    def __init__(self, value):
        self.s = value
        if value in openers or value in closers:
            self.balanced = False
        else:
            self.balanced = True

    def __str__(self):
        return self.s

    def __repr__(self):
        if not self.balanced:
            return self.s + '!'
        return self.s