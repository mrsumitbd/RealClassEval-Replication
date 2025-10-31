
from dataclasses import dataclass, fields
from typing import Any, Dict


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary with sensitive data masked.'''
        sensitive_keys = {
            'password', 'pwd', 'pass', 'secret', 'api_key', 'token',
            'access_token', 'bearer_token', 'auth', 'credentials',
            'credential', 'key', 'client_secret', 'client_id'
        }
        result: Dict[str, Any] = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if f.name.lower() in sensitive_keys:
                result[f.name] = '****'
            else:
                result[f.name] = value
        return result

    def __repr__(self) -> str:
        '''Safe representation without credentials.'''
        return f"{self.__class__.__name__}({self.to_dict()!r})"

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        return str(self.to_dict())
