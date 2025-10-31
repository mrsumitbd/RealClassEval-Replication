from typing import Any, Dict, List, Optional
from dataclasses import dataclass

@dataclass
class MCPResource:
    """Represents an MCP resource."""
    uri: str
    name: str
    description: str
    mime_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPResource':
        """Create a Resource from a dictionary."""
        return cls(uri=data.get('uri', ''), name=data.get('name', ''), description=data.get('description', ''), mime_type=data.get('mimeType') or data.get('mime_type'))

    def to_dict(self) -> Dict[str, Any]:
        """Convert the resource to a dictionary."""
        result = {'uri': self.uri, 'name': self.name, 'description': self.description}
        if self.mime_type:
            result['mimeType'] = self.mime_type
        return result