
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional


@dataclass
class RegistryConfig:
    """Configuration for a Schema Registry instance."""

    host: str
    port: int = 8081
    username: Optional[str] = None
    password: Optional[str] = None
    api_key: Optional[str] = None
    ssl: bool = False
    # any other optional settings can be added here

    def _mask_sensitive(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Return a copy of data with sensitive fields masked."""
        masked = data.copy()
        for key in ("password", "api_key"):
            if key in masked and masked[key] is not None:
                masked[key] = "****"
        return masked

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with sensitive data masked."""
        raw = asdict(self)
        return self._mask_sensitive(raw)

    def __repr__(self) -> str:
        """Safe representation without credentials."""
        return f"{self.__class__.__name__}({self.to_dict()})"

    def __str__(self) -> str:
        """Safe string representation without credentials."""
        return self.__repr__()
