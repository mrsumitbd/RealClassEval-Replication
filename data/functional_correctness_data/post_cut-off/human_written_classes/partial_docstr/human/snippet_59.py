import importlib
import os
from typing import Dict, Any, Optional, List
from openmanus_rl.tools.base import BaseTool

class ToolRegistry:
    """Registry for managing and executing tools."""

    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self.tool_instances: Dict[str, Any] = {}

    def discover_tools(self, tools_dir: str='openmanus_rl/tools'):
        """Auto-discover all available tools in the tools directory."""
        tools_found = []
        for item in os.listdir(tools_dir):
            tool_path = os.path.join(tools_dir, item)
            if os.path.isdir(tool_path) and (not item.startswith('_')):
                tool_module_path = os.path.join(tool_path, 'tool.py')
                if os.path.exists(tool_module_path):
                    tools_found.append(item)
        print(f'Discovered tools: {tools_found}')
        return tools_found

    def load_tool(self, tool_name: str, model_string: Optional[str]=None) -> Optional[BaseTool]:
        """Load a specific tool by name."""
        try:
            module_path = f'openmanus_rl.tools.{tool_name}.tool'
            module = importlib.import_module(module_path)
            class_name = ''.join((word.capitalize() for word in tool_name.split('_')))
            if hasattr(module, class_name):
                tool_class = getattr(module, class_name)
            else:
                for name in dir(module):
                    obj = getattr(module, name)
                    if isinstance(obj, type) and issubclass(obj, BaseTool) and (obj != BaseTool):
                        tool_class = obj
                        break
                else:
                    print(f'No tool class found in {module_path}')
                    return None
            if tool_class.require_llm_engine and model_string:
                tool_instance = tool_class(model_string=model_string)
            else:
                tool_instance = tool_class()
            self.tools[tool_name] = tool_instance
            return tool_instance
        except Exception as e:
            print(f'Failed to load tool {tool_name}: {e}')
            return None

    def register_tool(self, name: str, tool: BaseTool):
        """Register a tool instance."""
        self.tools[name] = tool

    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> str:
        """Execute a tool with given parameters."""
        if tool_name not in self.tools:
            tool = self.load_tool(tool_name)
            if not tool:
                return f"Error: Tool '{tool_name}' not found"
        else:
            tool = self.tools[tool_name]
        try:
            if 'query' in params and 'text' in tool.input_types:
                params['text'] = params.pop('query')
            elif 'expression' in params and 'code' in tool.input_types:
                params['code'] = params.pop('expression')
            result = tool.execute(**params)
            if isinstance(result, dict):
                return str(result.get('output', result))
            else:
                return str(result)
        except Exception as e:
            return f'Error executing {tool_name}: {str(e)}'

    def list_tools(self) -> List[str]:
        """List all registered tools."""
        return list(self.tools.keys())

    def get_tool_info(self, tool_name: str) -> Dict[str, Any]:
        """Get metadata for a specific tool."""
        if tool_name in self.tools:
            return self.tools[tool_name].get_metadata()
        return {}