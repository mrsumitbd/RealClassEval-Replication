
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class RegistryConfig:

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} with attributes: {', '.join(f'{k}={v}' for k, v in self.__dict__.items())}"
