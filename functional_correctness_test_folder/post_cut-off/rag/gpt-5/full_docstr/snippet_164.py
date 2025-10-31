from typing import Dict, List, Optional, Type, Any
import threading


class ToolRegistry:
    """Registry for tools."""
    _instance = None
    _lock = threading.RLock()

    def __new__(cls):
        """Singleton pattern."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._tools: Dict[str, Type["BaseTool"]] = {}
                cls._instance._display_names: Dict[str, str] = {}
            return cls._instance

    def register(self, tool_cls: Type["BaseTool"]) -> None:
        """Register a tool."""
        if not isinstance(tool_cls, type):
            raise TypeError("tool_cls must be a class")
        name = self._resolve_tool_name(tool_cls)
        key = name.strip().lower()
        with self._lock:
            existing = self._tools.get(key)
            if existing is not None and existing is not tool_cls:
                raise ValueError(
                    f"Tool '{name}' is already registered with a different class.")
            self._tools[key] = tool_cls
            self._display_names[key] = name

    def get_tool(self, name: str) -> Optional[Type["BaseTool"]]:
        """Get a tool by name."""
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        key = name.strip().lower()
        with self._lock:
            return self._tools.get(key)

    def list_tools(self) -> List[str]:
        """List all registered tools."""
        with self._lock:
            return sorted(self._display_names.values())

    def get_all_tools(self) -> Dict[str, Type["BaseTool"]]:
        """Get all registered tools."""
        with self._lock:
            return {self._display_names[k]: v for k, v in self._tools.items()}

    def format_tool_descriptions(self) -> str:
        """Format tool descriptions for the LLM."""
        lines: List[str] = []
        for name in self.list_tools():
            tool_cls = self.get_tool(name)
            if tool_cls is None:
                continue
            desc = self._resolve_tool_description(tool_cls)
            if desc:
                lines.append(f"- {name}: {desc}")
            else:
                lines.append(f"- {name}")
        return "\n".join(lines)

    @staticmethod
    def _resolve_tool_name(tool_cls: Type["BaseTool"]) -> str:
        name = getattr(tool_cls, "name", None)
        if isinstance(name, str) and name.strip():
            return name.strip()
        return tool_cls.__name__

    @staticmethod
    def _resolve_tool_description(tool_cls: Type["BaseTool"]) -> str:
        desc = getattr(tool_cls, "description", None)
        if isinstance(desc, str) and desc.strip():
            return " ".join(desc.strip().split())
        doc = getattr(tool_cls, "__doc__", None)
        if isinstance(doc, str):
            doc_clean = " ".join(doc.strip().split())
            return doc_clean
        return ""
