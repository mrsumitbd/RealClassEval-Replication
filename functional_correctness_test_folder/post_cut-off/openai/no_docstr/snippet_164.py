
from typing import Type, Optional, List, Dict, Any

# Try to import BaseTool from langchain; fall back to a dummy base class if unavailable.
try:
    from langchain.tools import BaseTool
except Exception:  # pragma: no cover
    class BaseTool:  # type: ignore
        """Fallback BaseTool for type checking when langchain is not installed."""
        pass


class ToolRegistry:
    """
    A singleton registry for tool classes.

    Each tool class should provide a `name` attribute (or use the class name)
    and optionally a `description` attribute.
    """

    _instance: Optional["ToolRegistry"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._registry: Dict[str, Type[BaseTool]] = {}
        return cls._instance

    def register(self, tool_cls: Type[BaseTool]) -> None:
        """
        Register a tool class.

        Parameters
        ----------
        tool_cls : Type[BaseTool]
            The tool class to register.
        """
        name = getattr(tool_cls, "name", tool_cls.__name__)
        self._registry[name] = tool_cls

    def get_tool(self, name: str) -> Optional[Type[BaseTool]]:
        """
        Retrieve a registered tool class by name.

        Parameters
        ----------
        name : str
            The name of the tool.

        Returns
        -------
        Optional[Type[BaseTool]]
            The tool class if found, otherwise None.
        """
        return self._registry.get(name)

    def list_tools(self) -> List[str]:
        """
        List all registered tool names.

        Returns
        -------
        List[str]
            Sorted list of tool names.
        """
        return sorted(self._registry.keys())

    def get_all_tools(self) -> Dict[str, Type[BaseTool]]:
        """
        Get a copy of the entire registry.

        Returns
        -------
        Dict[str, Type[BaseTool]]
            Mapping of tool names to tool classes.
        """
        return dict(self._registry)

    def format_tool_descriptions(self) -> str:
        """
        Format a human‑readable description of all registered tools.

        Returns
        -------
        str
            A string with each tool name and its description on a separate line.
        """
        lines: List[str] = []
        for name in self.list_tools():
            tool_cls = self._registry[name]
            description = getattr(tool_cls, "description",
                                  "No description provided.")
            lines.append(f"{name}: {description}")
        return "\n".join(lines)
