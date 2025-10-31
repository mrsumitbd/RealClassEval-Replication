
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
        self.name_to_tool = {tool['name'].lower(): tool for tool in tools}

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        '''
        Internal single-agent tool selection logic.
        '''
        # Simple implementation: return first 'limit' tools
        # In a real implementation, this would use task_description to rank tools
        return self.tools[:limit]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        '''
        Internal multi-agent tool partitioning logic.
        '''
        if overlap:
            # Each agent gets all tools (overlapping)
            return [self.tools.copy() for _ in range(num_agents)]
        else:
            # Split tools evenly among agents
            partition_size = len(self.tools) // num_agents
            partitions = []
            for i in range(num_agents):
                start = i * partition_size
                end = (i + 1) * partition_size if i < num_agents - \
                    1 else len(self.tools)
                partitions.append(self.tools[start:end])
            return partitions

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        '''Select tools by their names (case-insensitive).'''
        selected = []
        for name in tool_names:
            tool = self.name_to_tool.get(name.lower())
            if tool:
                selected.append(tool)
        return selected

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        '''Filter tools for each role based on name patterns.'''
        result = {}
        for role, patterns in role_patterns.items():
            matched_tools = []
            for tool in self.tools:
                for pattern in patterns:
                    if re.search(pattern, tool['name'], re.IGNORECASE):
                        matched_tools.append(tool)
                        break
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
        matched = []
        for tool in self.tools:
            matches = 0
            for kw in keywords:
                if (kw.lower() in tool['name'].lower() or
                        kw.lower() in tool.get('description', '').lower()):
                    matches += 1
            if (match_all and matches == len(keywords)) or (not match_all and matches > 0):
                matched.append(tool)
        return matched

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
