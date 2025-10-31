
from typing import Type, Optional, List, Dict


class ToolRegistry:
    _instance = None

    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._registry = {}
        return cls._instance

    def register(self, tool_cls: Type) -> None:
        """Register a tool class."""
        name = getattr(tool_cls, "name", tool_cls.__name__)
        self._registry[name] = tool_cls

    def get_tool(self, name: str) -> Optional[Type]:
        """Get a tool by name."""
        return self._registry.get(name)

    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self._registry.keys())

    def get_all_tools(self) -> Dict[str, Type]:
        """Return the entire registry mapping."""
        return dict(self._registry)

    def format_tool_descriptions(self) -> str:
        """Return a formatted string of tool names and descriptions."""
        lines = []
        for name, cls in self._registry.items():
            description = getattr(cls, "description", cls.__doc__ or "")
            description = description.strip() if description else ""
            lines.append(f"{name}: {description}")
        return "\n".join(lines)
