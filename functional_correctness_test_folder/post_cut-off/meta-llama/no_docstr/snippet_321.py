
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class RegistryConfig:
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def __repr__(self) -> str:
        return f"RegistryConfig({self.to_dict()})"

    def __str__(self) -> str:
        config_dict = self.to_dict()
        config_str = ", ".join(
            f"{key}={value}" for key, value in config_dict.items())
        return f"RegistryConfig({config_str})"
