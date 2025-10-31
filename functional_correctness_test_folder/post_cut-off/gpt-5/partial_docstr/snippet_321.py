from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Union


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''
    url: str = ""
    username: Optional[str] = None
    password: Optional[str] = None
    api_key: Optional[str] = None
    token: Optional[str] = None
    ssl_verify: Union[bool, str] = True
    timeout: Optional[float] = 10.0
    headers: Optional[Dict[str, str]] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    _SENSITIVE_KEYS = {
        "password",
        "api_key",
        "token",
        "authorization",
        "auth",
        "access_token",
        "secret",
        "client_secret",
        "bearer",
        "apikey",
        "x-api-key",
    }

    def to_dict(self) -> Dict[str, Any]:
        base: Dict[str, Any] = {
            "url": self.url,
            "username": self.username,
            "password": self.password,
            "api_key": self.api_key,
            "token": self.token,
            "ssl_verify": self.ssl_verify,
            "timeout": self.timeout,
            "headers": dict(self.headers) if self.headers is not None else None,
        }
        # Drop Nones
        base = {k: v for k, v in base.items() if v is not None}
        # Merge extras without overriding explicit fields
        for k, v in self.extra.items():
            if k not in base:
                base[k] = v
        return base

    def __repr__(self) -> str:
        redacted = self._redacted_dict(remove=False)
        items = ", ".join(f"{k}={repr(v)}" for k, v in redacted.items())
        return f"{self.__class__.__name__}({items})"

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        safe = self._redacted_dict(remove=True)
        items = ", ".join(f"{k}={repr(v)}" for k, v in safe.items())
        return f"{self.__class__.__name__}({items})"

    def _redacted_dict(self, remove: bool) -> Dict[str, Any]:
        d = self.to_dict()

        def sanitize(value: Any) -> Any:
            if isinstance(value, dict):
                return {
                    k: ("***" if (self._is_sensitive_key(k)
                        and not remove) else sanitize(v))
                    for k, v in value.items()
                    if not (remove and self._is_sensitive_key(k))
                }
            return value

        cleaned: Dict[str, Any] = {}
        for k, v in d.items():
            if self._is_sensitive_key(k):
                if not remove:
                    cleaned[k] = "***"
                # if remove=True, omit key entirely
                continue if remove else None
            cleaned[k] = sanitize(v)
        # Ensure deterministic order for repr/str
        return dict(sorted(cleaned.items(), key=lambda x: x[0]))

    def _is_sensitive_key(self, key: str) -> bool:
        k = key.lower().replace("-", "_")
        return k in self._SENSITIVE_KEYS
