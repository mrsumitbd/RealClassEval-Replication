from __future__ import annotations

from typing import Dict, List, Optional, Type, Any


class ToolRegistry:
    _instance: Optional["ToolRegistry"] = None

    def __new__(cls):
        '''Singleton pattern.'''
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools: Dict[str, Type["BaseTool"]] = {}
        return cls._instance

    def register(self, tool_cls: Type["BaseTool"]) -> None:
        name = getattr(tool_cls, "name", None)
        if not isinstance(name, str) or not name.strip():
            name = tool_cls.__name__
        self._tools[name] = tool_cls

    def get_tool(self, name: str) -> Optional[Type["BaseTool"]]:
        '''Get a tool by name.'''
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        '''List all registered tools.'''
        return list(self._tools.keys())

    def get_all_tools(self) -> Dict[str, Type["BaseTool"]]:
        return dict(self._tools)

    def format_tool_descriptions(self) -> str:
        items = []
        for name in sorted(self._tools.keys()):
            tool_cls = self._tools[name]
            desc = getattr(tool_cls, "description", None)
            if not isinstance(desc, str) or not desc.strip():
                desc = (tool_cls.__doc__ or "").strip()
            first_line = desc.strip().splitlines()[0] if desc else ""
            if first_line:
                items.append(f"{name}: {first_line}")
            else:
                items.append(f"{name}")
        return "\n".join(items)
