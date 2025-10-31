from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Dict, Iterable


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''

    # Add fields as needed, e.g.:
    # url: str = ""
    # username: str | None = None
    # password: str | None = None
    # api_key: str | None = None
    # verify_ssl: bool = True

    _SENSITIVE_PATTERNS: Iterable[str] = (
        "password",
        "secret",
        "token",
        "api_key",
        "apikey",
        "auth",
        "authorization",
        "credentials",
        "access_key",
        "accesskey",
        "client_secret",
        "private_key",
        "passphrase",
        "refresh_token",
        "session_key",
        "key",  # keep last to avoid over-masking but include generic coverage
    )

    def _is_sensitive_key(self, key: str) -> bool:
        k = key.lower()
        return any(p in k for p in self._SENSITIVE_PATTERNS)

    def _mask_scalar(self, value: Any) -> Any:
        if value is None:
            return None
        return "******"

    def _mask_value(self, key: str, value: Any) -> Any:
        if self._is_sensitive_key(key):
            return self._mask_scalar(value)

        # Recurse into structures
        if is_dataclass(value):
            # If the nested dataclass has to_dict, use it to preserve its own masking rules
            if hasattr(value, "to_dict") and callable(getattr(value, "to_dict")):
                return value.to_dict()
            # Otherwise, manually walk its fields
            out: Dict[str, Any] = {}
            for f in fields(value):
                v = getattr(value, f.name)
                out[f.name] = self._mask_value(f.name, v)
            return out

        if isinstance(value, dict):
            return {k: self._mask_value(str(k), v) for k, v in value.items()}

        if isinstance(value, (list, tuple, set)):
            # Without keys, we can't determine sensitivity for scalars,
            # but we still mask nested dicts/dataclasses within sequences.
            masked = []
            for item in value:
                if isinstance(item, dict):
                    masked.append({k: self._mask_value(str(k), v)
                                  for k, v in item.items()})
                elif is_dataclass(item):
                    if hasattr(item, "to_dict") and callable(getattr(item, "to_dict")):
                        masked.append(item.to_dict())
                    else:
                        nested: Dict[str, Any] = {}
                        for f in fields(item):
                            nested[f.name] = self._mask_value(
                                f.name, getattr(item, f.name))
                        masked.append(nested)
                else:
                    masked.append(item)
            # Preserve original collection type
            if isinstance(value, list):
                return masked
            if isinstance(value, tuple):
                return tuple(masked)
            return set(masked)

        # Leave other types as-is
        return value

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary with sensitive data masked.'''
        masked: Dict[str, Any] = {}
        for f in fields(self):
            # Skip private/dunder and class-private config fields if any
            if f.name.startswith("_"):
                continue
            val = getattr(self, f.name)
            masked[f.name] = self._mask_value(f.name, val)
        return masked

    def __repr__(self) -> str:
        '''Safe representation without credentials.'''
        items = ", ".join(f"{k}={repr(v)}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({items})"

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        return self.__repr__()
