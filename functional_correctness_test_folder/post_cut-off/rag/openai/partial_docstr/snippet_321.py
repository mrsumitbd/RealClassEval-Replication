
from __future__ import annotations

from dataclasses import dataclass, fields, asdict
from typing import Any, Dict, Iterable


def _is_sensitive(name: str) -> bool:
    """Return True if the field name looks like it contains sensitive data."""
    name_lower = name.lower()
    return any(
        keyword in name_lower
        for keyword in ("password", "secret", "token", "key", "credential", "api_key")
    )


def _mask_value(value: Any) -> Any:
    """Mask a value that is considered sensitive."""
    if isinstance(value, (str, bytes)):
        return "***"
    return value


@dataclass
class RegistryConfig:
    """Configuration for a Schema Registry instance."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with sensitive data masked."""
        raw = asdict(self)
        masked: Dict[str, Any] = {}
        for key, val in raw.items():
            if _is_sensitive(key):
                masked[key] = _mask_value(val)
            else:
                masked[key] = val
        return masked

    def __repr__(self) -> str:
        """Safe representation without credentials."""
        cls_name = self.__class__.__name__
        masked = self.to_dict()
        items = ", ".join(f"{k}={v!r}" for k, v in masked.items())
        return f"{cls_name}({items})"

    def __str__(self) -> str:
        """Safe string representation without credentials."""
        return self.__repr__()
