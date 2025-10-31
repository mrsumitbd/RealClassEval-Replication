
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class RegistryConfig:
    """Configuration for a Schema Registry instance."""

    host: str
    port: int = 8081
    username: Optional[str] = None
    password: Optional[str] = None
    ssl: bool = False
    # Additional optional fields can be added here if needed

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the configuration."""
        return {
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "ssl": self.ssl,
        }

    def __repr__(self) -> str:
        """Return an unambiguous representation of the object."""
        fields = ", ".join(f"{k}={v!r}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({fields})"

    def __str__(self) -> str:
        """Safe string representation without credentials."""
        safe_dict = self.to_dict()
        if safe_dict.get("password") is not None:
            safe_dict["password"] = "****"
        fields = ", ".join(f"{k}={v!r}" for k, v in safe_dict.items())
        return f"{self.__class__.__name__}({fields})"
