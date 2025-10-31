
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''
    url: str = ""
    username: Optional[str] = None
    password: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # Optionally, remove None values
        return {k: v for k, v in d.items() if v is not None}

    def __repr__(self) -> str:
        return (f"RegistryConfig(url={self.url!r}, username={self.username!r}, "
                f"password={'***' if self.password else None!r}, extra={self.extra!r})")

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        return (f"RegistryConfig(url={self.url!r}, "
                f"username={self.username!r}, "
                f"extra={self.extra!r})")
