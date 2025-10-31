
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary with sensitive data masked.'''
        config_dict = asdict(self)
        sensitive_keys = ['password', 'api_key', 'secret']
        for key in sensitive_keys:
            if key in config_dict:
                config_dict[key] = '*****'
        return config_dict

    def __repr__(self) -> str:
        '''Safe representation without credentials.'''
        config_dict = self.to_dict()
        return f"RegistryConfig({', '.join(f'{k}={v}' for k, v in config_dict.items())})"

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        config_dict = self.to_dict()
        return f"RegistryConfig: {', '.join(f'{k}={v}' for k, v in config_dict.items())}"
