
from typing import List, Dict, Any, Optional
import re


class ToolSelector:

    def __init__(self, tools: List[Dict[str, Any]]):
        '''
        Initialize with available tools.
        Args:
            tools: List of tool definitions from ToolManager
        '''
        self.tools = tools

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        '''
        Select tools relevant to the task description.
        Args:
            task_description: Description of the task
            limit: Maximum number of tools to return
        Returns:
            List of selected tools
        '''
        # Placeholder: Implement task-based selection logic
        return self.tools[:limit]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        '''
        Partition tools among multiple agents.
        Args:
            num_agents: Number of agents
            overlap: Whether tools can overlap between agents
            task_description: Optional task description for filtering
        Returns:
            List of tool lists, one per agent
        '''
        selected_tools = self._select_for_task(task_description, limit=len(
            self.tools)) if task_description else self.tools
        if overlap:
            return [selected_tools.copy() for _ in range(num_agents)]
        else:
            partition_size = len(selected_tools) // num_agents
            return [selected_tools[i*partition_size:(i+1)*partition_size] for i in range(num_agents)]

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        '''Select tools by their names (case-insensitive).'''
        tool_names_lower = [name.lower() for name in tool_names]
        return [tool for tool in self.tools if tool.get('name', '').lower() in tool_names_lower]

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        '''
        Filter tools by roles.
        Args:
            role_patterns: Dictionary mapping role names to regex patterns
        Returns:
            Dictionary mapping role names to matching tools
        '''
        result = {}
        for role, patterns in role_patterns.items():
            compiled_patterns = [re.compile(
                pattern, re.IGNORECASE) for pattern in patterns]
            matching_tools = []
            for tool in self.tools:
                tool_roles = tool.get('roles', [])
                if any(any(pattern.match(role) for pattern in compiled_patterns) for role in tool_roles):
                    matching_tools.append(tool)
            result[role] = matching_tools
        return result

    def filter_by_keywords(self, keywords: List[str], match_all: bool = False) -> List[Any]:
        '''
        Filter tools by keywords.
        Args:
            keywords: List of keywords to match
            match_all: Whether all keywords must match (default: any)
        Returns:
            List of matching tools
        '''
        keyword_set = {keyword.lower() for keyword in keywords}
        matching_tools = []
        for tool in self.tools:
            tool_text = ' '.join(
                str(value) for key, value in tool.items() if key != 'roles').lower()
            if match_all:
                if all(keyword in tool_text for keyword in keyword_set):
                    matching_tools.append(tool)
            else:
                if any(keyword in tool_text for keyword in keyword_set):
                    matching_tools.append(tool)
        return matching_tools

    def select_tools(self, task_description: str, num_agents: Optional[int] = None, overlap: bool = False, limit: int = 5) -> Any:
        '''
        Unified public interface for tool selection.
        - Single-agent (num_agents None or <=1): returns a flat list of top tools.
        - Multi-agent (num_agents >1): returns a list of tool lists, one per agent.
        Override this method to implement any custom logic.
        '''
        if num_agents is None or num_agents <= 1:
            return self._select_for_task(task_description, limit)
        else:
            return self._partition_tools_for_multi_agent(num_agents, overlap, task_description)
