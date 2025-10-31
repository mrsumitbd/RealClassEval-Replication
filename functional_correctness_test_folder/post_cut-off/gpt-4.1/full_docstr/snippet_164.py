
from typing import Type, Optional, List, Dict


class BaseTool:
    '''Base class for tools.'''
    name: str = ""
    description: str = ""


class ToolRegistry:
    '''Registry for tools.'''

    _instance = None
    _tools: Dict[str, Type[BaseTool]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._tools = {}
        return cls._instance

    def register(self, tool_cls: Type[BaseTool]) -> None:
        if not hasattr(tool_cls, 'name') or not tool_cls.name:
            raise ValueError("Tool class must have a 'name' attribute.")
        self._tools[tool_cls.name] = tool_cls

    def get_tool(self, name: str) -> Optional[Type[BaseTool]]:
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        return list(self._tools.keys())

    def get_all_tools(self) -> Dict[str, Type[BaseTool]]:
        return dict(self._tools)

    def format_tool_descriptions(self) -> str:
        descriptions = []
        for tool_cls in self._tools.values():
            desc = getattr(tool_cls, 'description', '')
            name = getattr(tool_cls, 'name', '')
            descriptions.append(f"{name}: {desc}")
        return "\n".join(descriptions)
