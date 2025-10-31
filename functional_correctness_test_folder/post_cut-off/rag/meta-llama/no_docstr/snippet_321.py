
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class RegistryConfig:
    """Configuration for a Schema Registry instance."""
    url: str
    username: str = None
    password: str = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with sensitive data masked."""
        config_dict = asdict(self)
        if config_dict.get('username'):
            config_dict['username'] = '*****'
        if config_dict.get('password'):
            config_dict['password'] = '*****'
        return config_dict

    def __repr__(self) -> str:
        """Safe representation without credentials."""
        return str(self.to_dict())

    def __str__(self) -> str:
        """Safe string representation without credentials."""
        return str(self.to_dict())
