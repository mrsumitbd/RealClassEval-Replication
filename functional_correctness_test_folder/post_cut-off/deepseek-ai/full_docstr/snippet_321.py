
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary with sensitive data masked.'''
        data = asdict(self)
        for key, value in data.items():
            if 'password' in key.lower() or 'secret' in key.lower() or 'token' in key.lower():
                data[key] = '*****'
        return data

    def __repr__(self) -> str:
        '''Safe representation without credentials.'''
        data = self.to_dict()
        return f"{self.__class__.__name__}({data})"

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        return repr(self)
