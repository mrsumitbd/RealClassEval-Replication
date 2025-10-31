
from dataclasses import dataclass, field
from typing import Any, Dict, Type, TypeVar

T = TypeVar('T', bound='MCPTool')


@dataclass
class MCPTool:
    """Represents an MCP tool."""
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Create an MCPTool instance from a dictionary.

        Parameters
        ----------
        data : Dict[str, Any]
            Dictionary containing at least 'name' and 'description'.
            'parameters' is optional and defaults to an empty dict.

        Returns
        -------
        MCPTool
            The constructed MCPTool instance.
        """
        name = data.get('name')
        description = data.get('description')
        parameters = data.get('parameters', {})
        if name is None or description is None:
            raise ValueError("Both 'name' and 'description' must be provided")
        return cls(name=name, description=description, parameters=parameters)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the MCPTool instance to a plain dictionary.

        Returns
        -------
        Dict[str, Any]
            Dictionary representation of the tool.
        """
        return {
            'name': self.name,
            'description': self.description,
            'parameters': self.parameters,
        }

    def to_tool_schema(self) -> Dict[str, Any]:
        """
        Convert the MCPTool instance to a tool schema suitable for
        OpenAI function calling.

        Returns
        -------
        Dict[str, Any]
            Tool schema dictionary.
        """
        return {
            'type': 'function',
            'function': {
                'name': self.name,
                'description': self.description,
                'parameters': self.parameters,
            },
        }
