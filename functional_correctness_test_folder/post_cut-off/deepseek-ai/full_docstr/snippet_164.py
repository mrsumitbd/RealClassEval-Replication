
from typing import Type, Optional, List, Dict
from abc import ABC


class BaseTool(ABC):
    pass


class ToolRegistry:
    '''Registry for tools.'''
    _instance = None
    _tools: Dict[str, Type[BaseTool]] = {}

    def __new__(cls):
        '''Singleton pattern.'''
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(self, tool_cls: Type[BaseTool]) -> None:
        '''Register a tool.'''
        self._tools[tool_cls.__name__] = tool_cls

    def get_tool(self, name: str) -> Optional[Type[BaseTool]]:
        '''Get a tool by name.'''
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        '''List all registered tools.'''
        return list(self._tools.keys())

    def get_all_tools(self) -> Dict[str, Type[BaseTool]]:
        '''Get all registered tools.'''
        return self._tools.copy()

    def format_tool_descriptions(self) -> str:
        '''Format tool descriptions for the LLM.'''
        descriptions = []
        for name, tool_cls in self._tools.items():
            doc = tool_cls.__doc__ or "No description available."
            descriptions.append(f"{name}: {doc.strip()}")
        return "\n".join(descriptions)
