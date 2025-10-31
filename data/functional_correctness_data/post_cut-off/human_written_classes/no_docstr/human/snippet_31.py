class Set:

    def __init__(self) -> None:
        self.sum = 0
        self.items = []

    def add(self, idx: int, val: int):
        self.items.append((idx, val))
        self.sum += val

    def merge(self, other):
        for idx, val in other.items:
            self.items.append((idx, val))
            self.sum += val

    def __lt__(self, other):
        if self.sum != other.sum:
            return self.sum < other.sum
        if len(self.items) != len(other.items):
            return len(self.items) < len(other.items)
        return self.items < other.items