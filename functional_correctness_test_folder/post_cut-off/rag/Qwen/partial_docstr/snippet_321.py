
from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''
    url: str
    username: str
    password: str

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary with sensitive data masked.'''
        return {
            'url': self.url,
            'username': self.username,
            'password': '*****'
        }

    def __repr__(self) -> str:
        '''Safe representation without credentials.'''
        return f"RegistryConfig(url={self.url!r}, username={self.username!r}, password='*****')"

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        return f"RegistryConfig(url={self.url}, username={self.username}, password='*****')"
