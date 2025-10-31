
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''
    url: str = field(default="")
    username: Optional[str] = field(default=None)
    password: Optional[str] = field(default=None)
    token: Optional[str] = field(default=None)
    extra: Optional[Dict[str, Any]] = field(default=None)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary with sensitive data masked.'''
        result = asdict(self)
        for key in ['password', 'token']:
            if result.get(key) is not None:
                result[key] = '***'
        return result

    def __repr__(self) -> str:
        '''Safe representation without credentials.'''
        fields = self.to_dict()
        field_str = ', '.join(f"{k}={repr(v)}" for k, v in fields.items())
        return f"{self.__class__.__name__}({field_str})"

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        return self.__repr__()
