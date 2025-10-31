
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class MCPTool:
    """Represents an MCP tool."""

    # Basic tool metadata
    name: str
    description: str = ""

    # Parameters are defined as a list of dictionaries, each describing a parameter.
    # Each parameter dict should contain at least:
    #   - name (str)
    #   - type (str)  # e.g., "string", "integer", "boolean", etc.
    #   - description (str)
    #   - required (bool, optional)
    parameters: List[Dict[str, Any]] = field(default_factory=list)

    # Optional additional metadata
    metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPTool":
        """Create a Tool from a dictionary."""
        # Extract known keys, ignore unknown ones
        name = data.get("name")
        if name is None:
            raise ValueError("Missing required field 'name' in tool data")

        description = data.get("description", "")
        parameters = data.get("parameters", [])
        metadata = data.get("metadata")

        # Ensure parameters is a list of dicts
        if not isinstance(parameters, list):
            raise TypeError("'parameters' must be a list")

        return cls(
            name=name,
            description=description,
            parameters=parameters,
            metadata=metadata,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the tool to a dictionary."""
        # Use asdict to include all fields, then filter out None values
        result = asdict(self)
        # Remove keys with None values to keep the dict clean
        return {k: v for k, v in result.items() if v is not None}

    def to_tool_schema(self) -> Dict[str, Any]:
        """Convert the tool to a tool schema."""
        # The schema follows the OpenAI tool specification
        schema: Dict[str, Any] = {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }

        # Build properties and required lists from self.parameters
        for param in self.parameters:
            pname = param.get("name")
            if not pname:
                continue  # skip invalid entries

            ptype = param.get("type", "string")
            pdesc = param.get("description", "")
            required = param.get("required", False)

            schema["parameters"]["properties"][pname] = {
                "type": ptype,
                "description": pdesc,
            }
            if required:
                schema["parameters"]["required"].append(pname)

        # If no required fields, remove the key to keep schema minimal
        if not schema["parameters"]["required"]:
            del schema["parameters"]["required"]

        # Include any additional metadata if present
        if self.metadata:
            schema.update(self.metadata)

        return schema
