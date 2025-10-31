from __future__ import annotations

from typing import Dict, List, Optional, Type


class ToolRegistry:
    '''Registry for tools.'''

    _instance: Optional["ToolRegistry"] = None

    def __new__(cls):
        '''Singleton pattern.'''
        if cls._instance is None:
            inst = super().__new__(cls)
            inst._tools: Dict[str, Type["BaseTool"]] = {}
            cls._instance = inst
        return cls._instance

    def register(self, tool_cls: Type["BaseTool"]) -> None:
        '''Register a tool.'''
        if not isinstance(tool_cls, type):
            raise TypeError("tool_cls must be a class")

        try:
            Base = BaseTool  # type: ignore[name-defined]
            if not issubclass(tool_cls, Base):
                raise TypeError("tool_cls must be a subclass of BaseTool")
        except NameError:
            pass  # BaseTool not available at runtime; skip strict check

        name = getattr(tool_cls, "name", tool_cls.__name__)
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Tool must have a non-empty string name")

        self._tools[name] = tool_cls

    def get_tool(self, name: str) -> Optional[Type["BaseTool"]]:
        '''Get a tool by name.'''
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        '''List all registered tools.'''
        return sorted(self._tools.keys())

    def get_all_tools(self) -> Dict[str, Type["BaseTool"]]:
        '''Get all registered tools.'''
        return dict(self._tools)

    def format_tool_descriptions(self) -> str:
        '''Format tool descriptions for the LLM.'''
        lines: List[str] = []
        for name in sorted(self._tools.keys()):
            tool_cls = self._tools[name]
            desc = getattr(tool_cls, "description", None)
            if desc is None:
                desc = (tool_cls.__doc__ or "").strip()
            else:
                desc = str(desc).strip()
            if desc:
                lines.append(f"- {name}: {desc}")
            else:
                lines.append(f"- {name}")
        return "\n".join(lines)
