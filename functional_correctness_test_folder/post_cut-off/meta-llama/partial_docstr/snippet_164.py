
from typing import Type, Optional, List, Dict


class BaseTool:
    # Assuming BaseTool is defined elsewhere
    pass


class ToolRegistry:
    _instance = None

    def __new__(cls):
        '''Singleton pattern.'''
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._instance._tools = {}
        return cls._instance

    def register(self, tool_cls: Type[BaseTool]) -> None:
        self._tools[tool_cls.__name__] = tool_cls

    def get_tool(self, name: str) -> Optional[Type[BaseTool]]:
        '''Get a tool by name.'''
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        '''List all registered tools.'''
        return list(self._tools.keys())

    def get_all_tools(self) -> Dict[str, Type[BaseTool]]:
        return self._tools.copy()

    def format_tool_descriptions(self) -> str:
        return '\n'.join(f'{name}: {tool_cls.__doc__}' for name, tool_cls in self._tools.items())
