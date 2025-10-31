
from typing import List, Dict, Any, Optional
import re


class ToolSelector:
    '''
    Primary interface for tool selection across single-agent and multi-agent scenarios.
    Use `select_tools(task_description, num_agents=None, overlap=False, limit=5)` to pick or partition tools.
    Override `select_tools` to implement custom selection strategies.
    '''

    def __init__(self, tools: List[Dict[str, Any]]):
        '''
        Initialize with available tools.
        Args:
            tools: List of tool definitions from ToolManager
        '''
        self.tools = tools

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        '''
        Internal single-agent tool selection logic.
        '''
        # Placeholder for actual selection logic
        return self.tools[:limit]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        '''
        Internal multi-agent tool partitioning logic.
        '''
        # Placeholder for actual partitioning logic
        partition_size = len(self.tools) // num_agents
        partitions = [
            self.tools[i*partition_size:(i+1)*partition_size] for i in range(num_agents)]
        if len(self.tools) % num_agents != 0:
            partitions[-1].extend(self.tools[num_agents*partition_size:])
        return partitions

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        '''Select tools by their names (case-insensitive).'''
        selected_tools = []
        for tool in self.tools:
            if tool['name'].lower() in [name.lower() for name in tool_names]:
                selected_tools.append(tool)
        return selected_tools

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        '''Filter tools for each role based on name patterns.'''
        filtered_tools = {}
        for role, patterns in role_patterns.items():
            filtered_tools[role] = []
            for tool in self.tools:
                for pattern in patterns:
                    if re.search(pattern, tool['name'], re.IGNORECASE):
                        filtered_tools[role].append(tool)
                        break
        return filtered_tools

    def filter_by_keywords(self, keywords: List[str], match_all: bool = False) -> List[Any]:
        '''
        Filter tools that match specified keywords in name or description.
        Args:
            keywords: List of keywords to match
            match_all: If True, tools must match all keywords. If False, match any keyword.
        Returns:
            List of tools matching the criteria
        '''
        filtered_tools = []
        for tool in self.tools:
            tool_text = f"{tool['name']} {tool.get('description', '')}".lower()
            keyword_matches = [
                keyword.lower() in tool_text for keyword in keywords]
            if (match_all and all(keyword_matches)) or (not match_all and any(keyword_matches)):
                filtered_tools.append(tool)
        return filtered_tools

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
