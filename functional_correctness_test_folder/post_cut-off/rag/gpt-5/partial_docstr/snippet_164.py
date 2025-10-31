from __future__ import annotations

from threading import RLock
from typing import Type, Optional, List, Dict


class ToolRegistry:
    """Registry for tools."""

    _instance: Optional["ToolRegistry"] = None
    _lock: RLock = RLock()

    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._registry: Dict[str, Type["BaseTool"]] = {}
        return cls._instance

    def register(self, tool_cls: Type["BaseTool"]) -> None:
        """Register a tool."""
        name = getattr(tool_cls, "name", None) or tool_cls.__name__
        with self._lock:
            # Enforce case-insensitive uniqueness
            for existing_name, existing_cls in self._registry.items():
                if existing_name.lower() == name.lower():
                    if existing_cls is tool_cls:
                        return
                    raise ValueError(
                        f"Tool with name '{name}' already registered.")
            self._registry[name] = tool_cls

    def get_tool(self, name: str) -> Optional[Type["BaseTool"]]:
        """Get a tool by name."""
        with self._lock:
            for n, cls in self._registry.items():
                if n.lower() == name.lower():
                    return cls
        return None

    def list_tools(self) -> List[str]:
        """List all registered tools."""
        with self._lock:
            return sorted(self._registry.keys(), key=lambda s: s.lower())

    def get_all_tools(self) -> Dict[str, Type["BaseTool"]]:
        """Get all registered tools."""
        with self._lock:
            return dict(self._registry)

    def format_tool_descriptions(self) -> str:
        """Format tool descriptions for the LLM."""
        def _get_description(tool_cls: Type["BaseTool"]) -> str:
            desc = None
            for attr in ("description", "short_description", "desc", "help", "HELP"):
                if hasattr(tool_cls, attr):
                    candidate = getattr(tool_cls, attr)
                    desc = candidate() if callable(candidate) else candidate
                    if desc:
                        break
            if not desc:
                desc = tool_cls.__doc__ or ""
            return " ".join(str(desc).strip().split())

        lines: List[str] = []
        for name in self.list_tools():
            tool_cls = self._registry[name]
            desc = _get_description(tool_cls)
            lines.append(f"- {name}: {desc}" if desc else f"- {name}")
        return "\n".join(lines)
