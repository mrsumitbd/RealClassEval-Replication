from dataclasses import dataclass, field
from copy import deepcopy


@dataclass
class Tag:
    _values: dict = field(default_factory=dict, repr=False)

    def __init__(self, **kwargs):
        object.__setattr__(self, "_values", dict(kwargs))

    def __getattr__(self, name):
        try:
            return self._values[name]
        except KeyError as e:
            raise AttributeError(
                f"'Tag' object has no attribute '{name}'") from e

    def __setattr__(self, name, value):
        if name == "_values":
            object.__setattr__(self, name, value)
        else:
            self._values[name] = value

    def __repr__(self):
        items = ", ".join(f"{k}={v!r}" for k, v in self._values.items())
        return f"Tag({items})"

    def to_dict(self):
        return deepcopy(self._values)

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        return cls(**data)
