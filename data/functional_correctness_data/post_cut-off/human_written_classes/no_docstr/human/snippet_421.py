from dataclasses import dataclass

@dataclass(frozen=True)
class LineMatch:
    idx: int
    'The index of the line in some file.'
    distance: int
    'The Levenshtein distance between the line in some file and a reference line.'

    def __lt__(self, other):
        return self.distance < other.distance

    def __le__(self, other):
        return self.distance <= other.distance

    def __gt__(self, other):
        return self.distance > other.distance

    def __ge__(self, other):
        return self.distance >= other.distance

    def __eq__(self, other):
        return self.distance == other.distance