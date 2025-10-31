from typing import Optional, Tuple

class State:

    def __init__(self, items: list[Tuple[int, int]], k: int) -> None:
        self.k = k
        self.sets = [Set() for _ in range(k)]
        assert len(items) in [1, k], f'{len(items)} not in [1, {k}]'
        for i, (idx, seqlen) in enumerate(items):
            self.sets[i].add(idx=idx, val=seqlen)
        self.sets = sorted(self.sets, reverse=True)

    def get_partitions(self):
        partitions = []
        for i in range(len(self.sets)):
            cur_partition = []
            for idx, _ in self.sets[i].items:
                cur_partition.append(idx)
            partitions.append(cur_partition)
        return partitions

    def merge(self, other):
        for i in range(self.k):
            self.sets[i].merge(other.sets[self.k - 1 - i])
        self.sets = sorted(self.sets, reverse=True)

    @property
    def spread(self) -> int:
        return self.sets[0].sum - self.sets[-1].sum

    def __lt__(self, other):
        if self.spread != other.spread:
            return self.spread > other.spread
        return self.sets[0] > other.sets[0]

    def __repr__(self) -> str:
        repr_str = '['
        for i in range(self.k):
            if i > 0:
                repr_str += ','
            repr_str += '{'
            for j, (_, seqlen) in enumerate(self.sets[i].items):
                if j > 0:
                    repr_str += ','
                repr_str += str(seqlen)
            repr_str += '}'
        repr_str += ']'
        return repr_str