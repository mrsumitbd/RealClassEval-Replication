from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class MCPResource:
    """Represents an MCP resource."""
    uri: str
    name: Optional[str] = None
    description: Optional[str] = None
    mime_type: Optional[str] = None
    text: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPResource':
        """Create a Resource from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        uri = data.get("uri")
        if not isinstance(uri, str) or not uri:
            raise ValueError("uri must be a non-empty string")
        name = data.get("name")
        description = data.get("description")
        mime_type = data.get("mimeType", data.get("mime_type"))
        text = data.get("text")
        metadata = data.get("metadata") or data.get("meta") or {}
        if metadata is None:
            metadata = {}
        return cls(
            uri=uri,
            name=name,
            description=description,
            mime_type=mime_type,
            text=text,
            metadata=metadata,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the resource to a dictionary."""
        result: Dict[str, Any] = {"uri": self.uri}
        if self.name is not None:
            result["name"] = self.name
        if self.description is not None:
            result["description"] = self.description
        if self.mime_type is not None:
            result["mimeType"] = self.mime_type
        if self.text is not None:
            result["text"] = self.text
        if self.metadata:
            result["metadata"] = self.metadata
        return result
