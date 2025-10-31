class MatchCoordinate:

    def __init__(self, row, rank):
        self.index = row
        self.rank = rank

    def __eq__(self, other):
        return self.index == other.index and self.rank == other.rank

    def __hash__(self):
        return 10 * self.index + self.rank

    def __repr__(self):
        return str.format('MatchCoordinate(index = {}, rank = {})', self.index, self.rank)