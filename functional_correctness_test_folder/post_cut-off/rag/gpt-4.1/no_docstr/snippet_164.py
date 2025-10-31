from typing import Type, Optional, List, Dict


class ToolRegistry:
    '''Registry for tools.'''

    _instance = None
    _tools: Dict[str, Type['BaseTool']] = {}

    def __new__(cls):
        '''Singleton pattern.'''
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(self, tool_cls: Type['BaseTool']) -> None:
        '''Register a tool.'''
        name = getattr(tool_cls, 'name', tool_cls.__name__)
        self._tools[name] = tool_cls

    def get_tool(self, name: str) -> Optional[Type['BaseTool']]:
        '''Get a tool by name.'''
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        '''List all registered tools.'''
        return list(self._tools.keys())

    def get_all_tools(self) -> Dict[str, Type['BaseTool']]:
        '''Get all registered tools.'''
        return dict(self._tools)

    def format_tool_descriptions(self) -> str:
        '''Format tool descriptions for the LLM.'''
        descriptions = []
        for name, tool_cls in self._tools.items():
            desc = getattr(tool_cls, '__doc__', '') or ''
            desc = desc.strip().replace('\n', ' ')
            descriptions.append(f"{name}: {desc}")
        return '\n'.join(descriptions)
