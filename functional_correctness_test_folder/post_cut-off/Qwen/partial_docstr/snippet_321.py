
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''
    url: str
    username: str
    password: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def __repr__(self) -> str:
        return f"RegistryConfig(url={self.url!r}, username={self.username!r}, password={self.password!r})"

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        return f"RegistryConfig(url={self.url!r}, username={self.username!r})"
