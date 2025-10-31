from dataclasses import dataclass

@dataclass
class SparseVector:
    indices: list[int]
    values: list[float] | list[int] | None = None

    def __post_init__(self):
        assert self.values is None or len(self.indices) == len(self.values)

    def to_dict_old(self):
        d = {'indices': self.indices}
        if self.values is not None:
            d['values'] = self.values
        return d

    def to_dict(self):
        if self.values is None:
            raise ValueError('SparseVector.values is None')
        result = {}
        for i, v in zip(self.indices, self.values):
            result[str(i)] = v
        return result

    @staticmethod
    def from_dict(d):
        return SparseVector(d['indices'], d.get('values'))

    def __str__(self):
        return f"SparseVector(indices={self.indices}{('' if self.values is None else f', values={self.values}')})"

    def __repr__(self):
        return str(self)