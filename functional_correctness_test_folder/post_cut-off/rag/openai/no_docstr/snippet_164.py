
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

    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._registry = {}
        return cls._instance

    def register(self, tool_cls: Type[BaseTool]) -> None:
        """Register a tool."""
        name = getattr(tool_cls, "name", tool_cls.__name__)
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
