
from typing import Type, Optional, List, Dict
from .base_tool import BaseTool


class ToolRegistry:
    """Registry for tools."""
    _instance = None
    _tools: Dict[str, Type[BaseTool]] = {}

    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
        return cls._instance

    def register(self, tool_cls: Type[BaseTool]) -> None:
        """Register a tool."""
        self._tools[tool_cls.name] = tool_cls

    def get_tool(self, name: str) -> Optional[Type[BaseTool]]:
        """Get a tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        """List all registered tools."""
        return list(self._tools.keys())

    def get_all_tools(self) -> Dict[str, Type[BaseTool]]:
        """Get all registered tools."""
        return self._tools.copy()

    def format_tool_descriptions(self) -> str:
        """Format tool descriptions for the LLM."""
        tool_descriptions = []
        for tool_name, tool_cls in self._tools.items():
            tool_description = f'{tool_name}: {tool_cls.description}'
            tool_descriptions.append(tool_description)
        return '\n'.join(tool_descriptions)
