from dataclasses import dataclass, asdict, field
from typing import Any, Dict


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''
    url: str = field(default="")
    username: str = field(default="")
    password: str = field(default="")
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary with sensitive data masked.'''
        d = asdict(self)
        if 'password' in d:
            d['password'] = '***'
        if 'username' in d:
            d['username'] = '***'
        return d

    def __repr__(self) -> str:
        '''Safe representation without credentials.'''
        d = self.to_dict()
        return f"RegistryConfig({d})"

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        return self.__repr__()
