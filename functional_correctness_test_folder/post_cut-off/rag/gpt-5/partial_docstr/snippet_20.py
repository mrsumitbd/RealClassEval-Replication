from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class MCPResource:
    """Represents an MCP resource."""
    uri: str
    name: Optional[str] = None
    description: Optional[str] = None
    mime_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPResource':
        """Create a Resource from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")

        if 'uri' not in data or not isinstance(data['uri'], str):
            raise ValueError("resource dictionary must include a string 'uri'")

        # Known keys and normalization
        uri = data['uri']
        name = data.get('name')
        description = data.get('description')

        # Accept both 'mimeType' (spec) and 'mime_type' (pythonic)
        mime_type = data.get('mimeType', data.get('mime_type'))

        # Start with explicit 'metadata' if provided, else empty
        meta: Dict[str, Any] = {}
        if isinstance(data.get('metadata'), dict):
            meta.update(data['metadata'])

        # Capture any extra keys as metadata (without overriding reserved keys)
        reserved = {'uri', 'name', 'description',
                    'mimeType', 'mime_type', 'metadata'}
        for k, v in data.items():
            if k not in reserved and k not in meta:
                meta[k] = v

        return cls(uri=uri, name=name, description=description, mime_type=mime_type, metadata=meta)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the resource to a dictionary."""
        out: Dict[str, Any] = {'uri': self.uri}

        if self.name is not None:
            out['name'] = self.name
        if self.description is not None:
            out['description'] = self.description
        if self.mime_type is not None:
            out['mimeType'] = self.mime_type

        # Merge metadata without overwriting reserved keys
        for k, v in (self.metadata or {}).items():
            if k not in out:
                out[k] = v

        return out
