from typing import Any, Dict, List, Optional, Union
from dataclasses import asdict, dataclass

@dataclass
class RegistryConfig:
    """Configuration for a Schema Registry instance."""
    name: str
    url: str
    user: str = ''
    password: str = ''
    description: str = ''
    viewonly: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with sensitive data masked."""
        result = asdict(self)
        if result.get('password'):
            result['password'] = '***MASKED***'
        return result

    def __repr__(self) -> str:
        """Safe representation without credentials."""
        password_masked = '***MASKED***' if self.password else ''
        return f'RegistryConfig(name={self.name!r}, url={self.url!r}, user={self.user!r}, password={password_masked!r}, description={self.description!r}, viewonly={self.viewonly})'

    def __str__(self) -> str:
        """Safe string representation without credentials."""
        auth_info = f'user={self.user}' if self.user else 'no-auth'
        return f'Registry config: {self.name} at {self.url} ({auth_info})'