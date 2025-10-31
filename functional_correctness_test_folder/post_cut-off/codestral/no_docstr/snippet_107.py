
from dataclasses import dataclass


@dataclass
class Context:

    def __post_init__(self) -> None:
        pass

    def __len__(self) -> int:
        return len(self.__dict__)

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict) -> 'Context':
        return cls(**data)
