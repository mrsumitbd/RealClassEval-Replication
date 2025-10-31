
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class RegistryConfig:
    # Example fields, you can modify as needed
    url: str = ""
    username: str = ""
    password: str = ""
    email: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
                f"url={self.url!r}, username={self.username!r}, "
                f"password={'***' if self.password else ''!r}, email={self.email!r})")

    def __str__(self) -> str:
        return f"RegistryConfig for {self.url} (user: {self.username})"
