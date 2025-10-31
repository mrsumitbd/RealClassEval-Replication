from __future__ import annotations

from typing import Dict, List, Optional, Type, Any


class ToolRegistry:
    _instance: Optional["ToolRegistry"] = None
    _tools: Dict[str, Type[Any]]

    def __new__(cls):
        if cls._instance is None:
            inst = super().__new__(cls)
            inst._tools = {}
            cls._instance = inst
        return cls._instance

    def register(self, tool_cls: Type["BaseTool"]) -> None:
        name = getattr(tool_cls, "name", None)
        if not isinstance(name, str) or not name:
            raise ValueError(
                "tool_cls must define a non-empty string attribute 'name'.")
        self._tools[name] = tool_cls

    def get_tool(self, name: str) -> Optional[Type["BaseTool"]]:
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        return sorted(self._tools.keys())

    def get_all_tools(self) -> Dict[str, Type["BaseTool"]]:
        return dict(self._tools)

    def format_tool_descriptions(self) -> str:
        lines: List[str] = []
        for name in self.list_tools():
            tool_cls = self._tools[name]
            desc = getattr(tool_cls, "description", None)
            if not isinstance(desc, str) or not desc:
                desc = (tool_cls.__doc__ or "").strip()
            lines.append(f"- {name}: {desc}" if desc else f"- {name}")
        return "\n".join(lines)
