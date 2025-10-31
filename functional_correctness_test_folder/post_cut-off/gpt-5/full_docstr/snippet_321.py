from dataclasses import dataclass, field, fields, asdict
from typing import Any, Dict, Optional, Union


def _is_sensitive_field(name: str) -> bool:
    n = name.lower()
    sensitive_keywords = (
        "password",
        "secret",
        "token",
        "key",
        "auth",
        "credential",
        "authorization",
        "private",
    )
    return any(k in n for k in sensitive_keywords)


def _mask_string(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    if value == "":
        return ""
    return "****"


def _mask_value(name: str, value: Any) -> Any:
    if _is_sensitive_field(name):
        if isinstance(value, (str, bytes, bytearray)):
            return _mask_string(value if isinstance(value, str) else str(value))
        # For non-string sensitive types, replace with masked marker
        if value is None:
            return None
        return "****"

    # For non-sensitive compound structures, recurse and mask inner sensitive keys
    if isinstance(value, dict):
        return {k: _mask_value(k, v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        # For sequences, we cannot infer key names; just pass through
        # but if elements are dicts, mask their sensitive keys
        def mask_elem(elem: Any) -> Any:
            if isinstance(elem, dict):
                return {k: _mask_value(k, v) for k, v in elem.items()}
            return elem

        seq = [mask_elem(e) for e in value]
        return type(value)(seq) if not isinstance(value, list) else seq
    return value


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''

    url: str = ""
    username: Optional[str] = None
    password: Optional[str] = field(default=None, repr=False)
    api_key: Optional[str] = field(default=None, repr=False)
    api_secret: Optional[str] = field(default=None, repr=False)
    ssl_verify: Union[bool, str] = True
    timeout: Optional[float] = None
    request_headers: Optional[Dict[str, str]] = None
    extra: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary with sensitive data masked.'''
        raw = asdict(self)
        masked: Dict[str, Any] = {}
        for f in fields(self):
            name = f.name
            value = raw.get(name)
            masked[name] = _mask_value(name, value)
        return masked

    def __repr__(self) -> str:
        '''Safe representation without credentials.'''
        masked = self.to_dict()
        args = ", ".join(f"{k}={repr(v)}" for k, v in masked.items())
        return f"{self.__class__.__name__}({args})"

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        return self.__repr__()
