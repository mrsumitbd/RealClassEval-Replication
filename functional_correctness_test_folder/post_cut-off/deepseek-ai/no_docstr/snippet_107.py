
from dataclasses import dataclass, asdict


@dataclass
class Context:

    def __post_init__(self) -> None:
        pass

    def __len__(self) -> int:
        return len(self.__dict__)

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return f"Context({self.__dict__})"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Context':
        return cls(**data)
