
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
        # Placeholder: Implement actual task-based selection logic
        return self.tools[:limit]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        '''
        Internal multi-agent tool partitioning logic.
        '''
        if overlap:
            return [self.tools.copy() for _ in range(num_agents)]
        else:
            partition_size = len(self.tools) // num_agents
            return [self.tools[i*partition_size:(i+1)*partition_size] for i in range(num_agents)]

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        '''Select tools by their names (case-insensitive).'''
        tool_names_lower = [name.lower() for name in tool_names]
        return [tool for tool in self.tools if tool.get('name', '').lower() in tool_names_lower]

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        '''Filter tools for each role based on name patterns.'''
        result = {}
        for role, patterns in role_patterns.items():
            compiled_patterns = [re.compile(
                pattern, re.IGNORECASE) for pattern in patterns]
            matched_tools = []
            for tool in self.tools:
                tool_name = tool.get('name', '')
                if any(pattern.search(tool_name) for pattern in compiled_patterns):
                    matched_tools.append(tool)
            result[role] = matched_tools
        return result

    def filter_by_keywords(self, keywords: List[str], match_all: bool = False) -> List[Any]:
        '''
        Filter tools that match specified keywords in name or description.
        Args:
            keywords: List of keywords to match
            match_all: If True, tools must match all keywords. If False, match any keyword.
        Returns:
            List of tools matching the criteria
        '''
        keywords_lower = [kw.lower() for kw in keywords]
        matched_tools = []
        for tool in self.tools:
            name = tool.get('name', '').lower()
            description = tool.get('description', '').lower()
            if match_all:
                if all(kw in name or kw in description for kw in keywords_lower):
                    matched_tools.append(tool)
            else:
                if any(kw in name or kw in description for kw in keywords_lower):
                    matched_tools.append(tool)
        return matched_tools

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
