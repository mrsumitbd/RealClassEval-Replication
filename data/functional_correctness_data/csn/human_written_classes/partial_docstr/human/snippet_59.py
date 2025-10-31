class HashableTuple:
    """Overcomes non-hashability of symbolic elements"""

    def __init__(self, elements: tuple):
        self.elements = elements

    def __iter__(self):
        yield from self.elements

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, item):
        return self.elements[item]