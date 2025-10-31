
from __future__ import annotations

from typing import Type, Optional, List, Dict

# Assume BaseTool is defined elsewhere in the package.
# It should expose at least `name` and `description` attributes.
# If those attributes are missing, we fall back to the class name and a generic description.
try:
    from .base_tool import BaseTool  # type: ignore
except Exception:  # pragma: no cover
    # Fallback definition for type checking / documentation purposes
    class BaseTool:  # pragma: no cover
        name: str
        description: str


class ToolRegistry:
    """Registry for tools."""

    _instance: Optional["ToolRegistry"] = None

    def __new__(cls) -> "ToolRegistry":
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools: Dict[str, Type[BaseTool]] = {}
        return cls._instance

    def register(self, tool_cls: Type[BaseTool]) -> None:
        """Register a tool."""
        name = getattr(tool_cls, "name", tool_cls.__name__)
        self._tools[name] = tool_cls

    def get_tool(self, name: str) -> Optional[Type[BaseTool]]:
        """Get a tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        """List all registered tools."""
        return sorted(self._tools.keys())

    def get_all_tools(self) -> Dict[str, Type[BaseTool]]:
        """Get all registered tools."""
        return dict(self._tools)

    def format_tool_descriptions(self) -> str:
        """Format tool descriptions for the LLM."""
        lines: List[str] = []
        for name, tool_cls in sorted(self._tools.items()):
            description = getattr(tool_cls, "description",
                                  "No description provided.")
            lines.append(f"{name}: {description}")
        return "\n".join(lines)
