
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping


@dataclass
class MCPTool:
    """Represents an MCP tool."""

    # Basic tool attributes
    name: str
    tool_id: str
    description: str | None = None
    # Optional parameters that may be required by the tool
    parameters: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MCPTool":
        """
        Create a Tool from a dictionary.

        The dictionary may contain any of the following keys:
            - name
            - tool_id
            - description
            - parameters

        Missing keys are filled with sensible defaults.
        """
        # Extract known keys with defaults
        name = data.get("name", "")
        tool_id = data.get("tool_id", "")
        description = data.get("description")
        parameters = data.get("parameters", {})

        # Ensure parameters is a dict
        if not isinstance(parameters, dict):
            raise TypeError(
                f"parameters must be a dict, got {type(parameters).__name__}"
            )

        return cls(name=name, tool_id=tool_id, description=description, parameters=parameters)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the tool to a dictionary.

        The resulting dictionary contains all attributes of the tool,
        excluding any that are None.
        """
        result: Dict[str, Any] = {
            "name": self.name,
            "tool_id": self.tool_id,
            "parameters": self.parameters,
        }
        if self.description is not None:
            result["description"] = self.description
        return result

    def to_tool_schema(self) -> Dict[str, Any]:
        """
        Convert the tool to a tool schema.

        The schema follows a simple JSON‑schema‑like structure:
            {
                "type": "tool",
                "id": <tool_id>,
                "name": <name>,
                "description": <description>,
                "parameters": <parameters>
            }
        """
        schema: Dict[str, Any] = {
            "type": "tool",
            "id": self.tool_id,
            "name": self.name,
            "parameters": self.parameters,
        }
        if self.description is not None:
            schema["description"] = self.description
        return schema
