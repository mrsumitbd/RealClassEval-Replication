
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in self.to_dict().items())})"

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        return f"{self.__class__.__name__}({', '.join(f'{k}=****' if 'password' in k.lower() or 'secret' in k.lower() else f'{k}={v}' for k, v in self.to_dict().items())})"
