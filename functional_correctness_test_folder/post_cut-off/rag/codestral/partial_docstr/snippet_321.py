
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional


@dataclass
class RegistryConfig:
    '''Configuration for a Schema Registry instance.'''
    url: str
    username: Optional[str] = None
    password: Optional[str] = None
    api_key: Optional[str] = None
    api_secret: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary with sensitive data masked.'''
        config_dict = asdict(self)
        if self.username:
            config_dict['username'] = '*****'
        if self.password:
            config_dict['password'] = '*****'
        if self.api_key:
            config_dict['api_key'] = '*****'
        if self.api_secret:
            config_dict['api_secret'] = '*****'
        return config_dict

    def __repr__(self) -> str:
        '''Safe representation without credentials.'''
        return f"RegistryConfig(url='{self.url}', username='*****', password='*****', api_key='*****', api_secret='*****')"

    def __str__(self) -> str:
        '''Safe string representation without credentials.'''
        return f"RegistryConfig(url='{self.url}', username='*****', password='*****', api_key='*****', api_secret='*****')"
