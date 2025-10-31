
from typing import Type, Optional, List, Dict


class ToolRegistry:
    '''Registry for tools.'''

    _instance: Optional["ToolRegistry"] = None
    _tools: Dict[str, Type["BaseTool"]] = {}

    def __new__(cls):
        '''Singleton pattern.'''
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(self, tool_cls: Type["BaseTool"]) -> None:
        '''Register a tool.'''
        name = getattr(tool_cls, "name", tool_cls.__name__)
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
        lines = []
        for name, cls in sorted(self._tools.items()):
            description = getattr(cls, "description", "")
            lines.append(f"{name}: {description}")
        return "\n".join(lines)
