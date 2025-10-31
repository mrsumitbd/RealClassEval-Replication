
from dataclasses import dataclass, asdict
from typing import Dict, Any
import pprint


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary with sensitive data masked.'''
        return asdict(self)

    def __repr__(self) -> str:
        '''Safe representation without credentials.'''
        return pprint.pformat(self.to_dict())

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        return self.__repr__()
