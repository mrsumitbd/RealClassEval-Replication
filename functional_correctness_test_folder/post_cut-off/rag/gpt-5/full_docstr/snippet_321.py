from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional

_MASK = "***"


@dataclass
class RegistryConfig:
    """Configuration for a Schema Registry instance."""
    url: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    token: Optional[str] = None
    basic_auth_user_info: Optional[str] = None  # e.g., "user:pass"
    ssl_cafile: Optional[str] = None
    ssl_certfile: Optional[str] = None
    ssl_keyfile: Optional[str] = None
    ssl_password: Optional[str] = None
    verify_ssl: Optional[bool] = True
    headers: Dict[str, str] = field(default_factory=dict)
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with sensitive data masked."""
        sensitive_keys = {
            "password",
            "passwd",
            "api_key",
            "api-secret",
            "api_secret",
            "secret",
            "token",
            "access_token",
            "refresh_token",
            "authorization",
            "basic_auth_user_info",
            "sasl_password",
            "ssl_password",
            "bearer_token",
            "client_secret",
        }

        def mask(obj: Any, parent_key: Optional[str] = None) -> Any:
            if isinstance(obj, dict):
                return {k: mask(v, k) for k, v in obj.items()}
            if isinstance(parent_key, str):
                key_lower = parent_key.lower()
                if key_lower in sensitive_keys:
                    return _MASK if obj is not None else None
            return obj

        return mask(asdict(self))

    def __repr__(self) -> str:
        """Safe representation without credentials."""
        safe = self.to_dict()
        # Deterministic ordering for readability
        items = ", ".join(f"{k}={safe[k]!r}" for k in sorted(safe.keys()))
        return f"RegistryConfig({items})"

    def __str__(self) -> str:
        """Safe string representation without credentials."""
        return self.__repr__()
