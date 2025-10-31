
from dataclasses import dataclass, fields
from typing import Dict, Any


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''
    url: str
    username: str
    password: str

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary with sensitive data masked.'''
        return {field.name: '*' * 8 if field.name in ['username', 'password'] else getattr(self, field.name) for field in fields(self)}

    def __repr__(self) -> str:
        '''Safe representation without credentials.'''
        return f"RegistryConfig(url={self.url!r}, username='********', password='********')"

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        return f"RegistryConfig(url={self.url}, username='********', password='********')"
