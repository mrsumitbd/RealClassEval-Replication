from dataclasses import dataclass, asdict, fields, is_dataclass
from typing import Any, Dict, Mapping, Sequence


_MASK = "****"


def _is_sensitive_field(name: str) -> bool:
    n = (name or "").lower()
    tokens = [
        "password",
        "passwd",
        "secret",
        "token",
        "api_key",
        "apikey",
        "api-secret",
        "api_secret",
        "access_token",
        "refresh_token",
        "client_secret",
        "secret_key",
        "private_key",
        "sasl_password",
        "bearer_token",
        "auth_token",
        "key",  # only when used with a separator or exactly 'key'
    ]

    # Exact matches for the common sensitive names.
    if n in tokens:
        return True

    # Match when the field name ends with a known sensitive token with separators.
    seps = ("_", "-", ".")
    for t in tokens:
        for sep in seps:
            if n.endswith(sep + t):
                return True

    return False


def _mask_value(value: Any, key_name: str | None = None) -> Any:
    # If the key itself is sensitive, mask the entire value.
    if key_name and _is_sensitive_field(key_name):
        return _MASK

    # Recursively traverse structures to mask nested sensitive entries.
    if is_dataclass(value):
        return _mask_mapping(asdict(value))
    if isinstance(value, Mapping):
        return _mask_mapping(value)
    if isinstance(value, (list, tuple, set)):
        # No key context for individual items; just recurse normally.
        t = type(value)
        return t(_mask_value(v) for v in value)

    return value


def _mask_mapping(mapping: Mapping[str, Any]) -> Dict[str, Any]:
    masked: Dict[str, Any] = {}
    for k, v in mapping.items():
        masked[k] = _mask_value(v, k)
    return masked


@dataclass
class RegistryConfig:
    """Configuration for a Schema Registry instance."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with sensitive data masked."""
        data = asdict(self) if is_dataclass(
            self) else dict(self)  # type: ignore[arg-type]
        return _mask_mapping(data)

    def __repr__(self) -> str:
        """Safe representation without credentials."""
        cls_name = self.__class__.__name__
        masked = self.to_dict()
        # Preserve field order as declared in dataclass
        try:
            ordered_keys = [f.name for f in fields(self)]
        except TypeError:
            ordered_keys = list(masked.keys())
        args = ", ".join(
            f"{k}={masked.get(k)!r}" for k in ordered_keys if k in masked)
        return f"{cls_name}({args})"

    def __str__(self) -> str:
        """Safe string representation without credentials."""
        return self.__repr__()
