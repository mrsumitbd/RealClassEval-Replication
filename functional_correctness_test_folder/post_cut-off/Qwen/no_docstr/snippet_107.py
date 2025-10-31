
from dataclasses import dataclass, fields


@dataclass
class Context:

    def __post_init__(self) -> None:
        pass

    def __len__(self) -> int:
        return len(fields(self))

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(f'{field.name}={getattr(self, field.name)!r}' for field in fields(self))})"

    def to_dict(self) -> dict:
        return {field.name: getattr(self, field.name) for field in fields(self)}

    @classmethod
    def from_dict(cls, data: dict) -> 'Context':
        return cls(**data)
