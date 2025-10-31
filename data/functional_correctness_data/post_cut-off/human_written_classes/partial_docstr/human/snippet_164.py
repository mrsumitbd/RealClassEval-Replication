from typing import Dict, Callable, Any, Optional, List

class ToolGroup:
    """
    A group of tools that can be used together.
    """

    def __init__(self, name: str):
        self.name = name
        self._tool_registry: Dict[str, Callable] = {}
        self._register_tools()

    def get_name(self):
        return self.name

    def _register_tools(self):
        for attr_name in dir(self):
            raw = getattr(type(self), attr_name, None)
            if isinstance(raw, tool):
                self._tool_registry[raw.name] = getattr(self, attr_name)

    def get_tool(self, name: str) -> Optional[Callable]:
        return self._tool_registry.get(name)

    def get_tool_names(self) -> List[str]:
        return list(self._tool_registry.keys())

    def execute_tool(self, name: str, *args, **kwargs) -> Any:
        tool_func = self.get_tool(name)
        if tool_func:
            return tool_func(*args, **kwargs)
        raise ValueError(f"Tool '{name}' not found in group '{self.name}'.")

    def get_tool_to_group_mapping(self) -> Dict[str, str]:
        return {name: self.name for name in self._tool_registry}