
from dataclasses import dataclass, asdict, fields
from typing import Any


@dataclass
class Context:
    def __post_init__(self) -> None:
        for field in fields(self):
            if not hasattr(self, field.name):
                setattr(self, field.name, field.default)

    def __len__(self) -> int:
        return len(asdict(self))

    def __str__(self) -> str:
        return str(asdict(self))

    def __repr__(self) -> str:
        attributes = ', '.join(
            f'{field.name}={getattr(self, field.name)}' for field in fields(self))
        return f'Context({attributes})'

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Context':
        field_names = [field.name for field in fields(cls)]
        filtered_data = {key: value for key,
                         value in data.items() if key in field_names}
        return cls(**filtered_data)
