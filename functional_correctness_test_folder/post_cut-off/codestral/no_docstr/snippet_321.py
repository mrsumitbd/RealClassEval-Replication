
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class RegistryConfig:

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.__dict__}"
