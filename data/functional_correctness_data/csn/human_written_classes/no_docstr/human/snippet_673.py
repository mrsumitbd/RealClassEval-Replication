class Filter:

    def __init__(self, inclusive=False, *items):
        self.inclusive = inclusive
        self.items = items

    def __contains__(self, x):
        if self.inclusive:
            result = x in self.items
        else:
            result = x not in self.items
        return result