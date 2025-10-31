
from dataclasses import dataclass, fields
from typing import Any, Dict


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''

    # Example fields – adjust as needed
    host: str = "localhost"
    port: int = 8081
    username: str | None = None
    password: str | None = None
    ssl: bool = False
    api_key: str | None = None

    def _mask_value(self, name: str, value: Any) -> Any:
        """Mask sensitive values."""
        sensitive_keywords = {
            "password",
            "pwd",
            "secret",
            "token",
            "apikey",
            "api_key",
            "access_token",
            "bearer_token",
            "credential",
            "credentials",
        }
        if name.lower() in sensitive_keywords:
            return "****"
        return value

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with sensitive data masked."""
        result: Dict[str, Any] = {}
        for f in fields(self):
            raw_value = getattr(self, f.name)
            result[f.name] = self._mask_value(f.name, raw_value)
        return result

    def __repr__(self) -> str:
        """Safe representation without credentials."""
        items = ", ".join(f"{k}={v!r}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({items})"

    def __str__(self) -> str:
        """Safe string representation without credentials."""
        return str(self.to_dict())
