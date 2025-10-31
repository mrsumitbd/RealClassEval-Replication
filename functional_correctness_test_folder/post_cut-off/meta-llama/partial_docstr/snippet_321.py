
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''
    url: str
    username: str = None
    password: str = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def __repr__(self) -> str:
        return f"RegistryConfig({self.url}, username={self.username}, password=*****)"

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        return f"RegistryConfig({self.url})"
