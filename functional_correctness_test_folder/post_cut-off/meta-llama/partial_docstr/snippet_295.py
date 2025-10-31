
from typing import List, Dict, Any, Optional


class ToolSelector:

    def __init__(self, tools: List[Dict[str, Any]]):
        '''
        Initialize with available tools.
        Args:
            tools: List of tool definitions from ToolManager
        '''
        self.tools = tools

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        # Simple implementation: return top tools based on task description similarity (not implemented here)
        # For demonstration, assume tools with 'description' key and return top 'limit' tools
        return sorted(self.tools, key=lambda x: task_description.lower() in x.get('description', '').lower(), reverse=True)[:limit]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        selected_tools = self._select_for_task(
            task_description, limit=num_agents*5) if task_description else self.tools
        if overlap:
            return [selected_tools[i::num_agents] for i in range(num_agents)]
        else:
            tools_per_agent = len(selected_tools) // num_agents
            return [selected_tools[i*tools_per_agent:(i+1)*tools_per_agent] for i in range(num_agents-1)] + [selected_tools[(num_agents-1)*tools_per_agent:]]

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        '''Select tools by their names (case-insensitive).'''
        tool_names = [name.lower() for name in tool_names]
        return [tool for tool in self.tools if tool['name'].lower() in tool_names]

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        result = {}
        for role, patterns in role_patterns.items():
            result[role] = [tool for tool in self.tools if any(pattern.lower() in tool.get(
                'description', '').lower() or pattern.lower() in tool['name'].lower() for pattern in patterns)]
        return result

    def filter_by_keywords(self, keywords: List[str], match_all: bool = False) -> List[Any]:
        keywords = [keyword.lower() for keyword in keywords]
        if match_all:
            return [tool for tool in self.tools if all(keyword in tool.get('description', '').lower() or keyword in tool['name'].lower() for keyword in keywords)]
        else:
            return [tool for tool in self.tools if any(keyword in tool.get('description', '').lower() or keyword in tool['name'].lower() for keyword in keywords)]

    def select_tools(self, task_description: str, num_agents: Optional[int] = None, overlap: bool = False, limit: int = 5) -> Any:
        '''
        Unified public interface for tool selection.
        - Single-agent (num_agents None or <=1): returns a flat list of top tools.
        - Multi-agent (num_agents >1): returns a list of tool lists, one per agent.
        Override this method to implement any custom logic.
        '''
        if num_agents is None or num_agents <= 1:
            return self._select_for_task(task_description, limit=limit)
        else:
            return self._partition_tools_for_multi_agent(num_agents, overlap=overlap, task_description=task_description)
