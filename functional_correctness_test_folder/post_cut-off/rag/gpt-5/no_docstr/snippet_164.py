from typing import Type, Optional, List, Dict


class ToolRegistry:
    """Registry for tools."""
    _instance: Optional["ToolRegistry"] = None

    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools: Dict[str, Type["BaseTool"]] = {}
        return cls._instance

    def register(self, tool_cls: Type["BaseTool"]) -> None:
        """Register a tool."""
        name = getattr(tool_cls, "name", None)
        if not isinstance(name, str) or not name:
            name = tool_cls.__name__
        existing = self._tools.get(name)
        if existing is not None and existing is not tool_cls:
            raise ValueError(
                f"Tool '{name}' is already registered with a different class.")
        self._tools[name] = tool_cls

    def get_tool(self, name: str) -> Optional[Type["BaseTool"]]:
        """Get a tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        """List all registered tools."""
        return sorted(self._tools.keys())

    def get_all_tools(self) -> Dict[str, Type["BaseTool"]]:
        """Get all registered tools."""
        return dict(self._tools)

    def format_tool_descriptions(self) -> str:
        """Format tool descriptions for the LLM."""
        lines: List[str] = []
        for name in self.list_tools():
            tool_cls = self._tools[name]
            desc = getattr(tool_cls, "description", None)
            if not isinstance(desc, str) or not desc.strip():
                doc = tool_cls.__doc__
                desc = doc.strip() if isinstance(doc, str) and doc else ""
            desc = " ".join(desc.split()) if desc else ""
            lines.append(f"- {name}: {desc}" if desc else f"- {name}")
        return "\n".join(lines)
