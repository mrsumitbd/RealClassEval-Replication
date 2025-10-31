
from __future__ import annotations

from typing import Type, Optional, List, Dict

# Assume BaseTool is defined elsewhere in the project.
# It should provide at least `name` and `description` attributes.
try:
    from .base_tool import BaseTool  # type: ignore
except Exception:  # pragma: no cover
    # Fallback for environments where the import path differs.
    from base_tool import BaseTool  # type: ignore


class ToolRegistry:
    """Registry for tools."""

    _instance: Optional["ToolRegistry"] = None
    _registry: Dict[str, Type[BaseTool]]

    def __new__(cls) -> "ToolRegistry":
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._registry = {}
        return cls._instance

    def register(self, tool_cls: Type[BaseTool]) -> None:
        """Register a tool."""
        if not hasattr(tool_cls, "name"):
            raise AttributeError(
                f"Tool class {tool_cls!r} must have a 'name' attribute")
        name = getattr(tool_cls, "name")
        if not isinstance(name, str):
            raise TypeError(
                f"Tool name must be a string, got {type(name).__name__}")
        self._registry[name] = tool_cls

    def get_tool(self, name: str) -> Optional[Type[BaseTool]]:
        """Get a tool by name."""
        return self._registry.get(name)

    def list_tools(self) -> List[str]:
        """List all registered tools."""
        return sorted(self._registry.keys())

    def get_all_tools(self) -> Dict[str, Type[BaseTool]]:
        """Get all registered tools."""
        return dict(self._registry)

    def format_tool_descriptions(self) -> str:
        """Format tool descriptions for the LLM."""
        lines: List[str] = []
        for name in self.list_tools():
            tool_cls = self._registry[name]
            description = getattr(tool_cls, "description", "")
            lines.append(f"{name}: {description}")
        return "\n".join(lines)
