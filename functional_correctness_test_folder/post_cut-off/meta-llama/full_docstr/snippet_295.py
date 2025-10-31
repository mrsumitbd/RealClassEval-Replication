
from typing import List, Dict, Any, Optional


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
        # Simple implementation: filter tools by keyword presence in task description
        # and return top 'limit' tools
        task_keywords = task_description.lower().split()
        scored_tools = [(tool, sum(1 for keyword in task_keywords if keyword in tool['name'].lower() or keyword in tool.get('description', '').lower()))
                        for tool in self.tools]
        scored_tools.sort(key=lambda x: x[1], reverse=True)
        return [tool for tool, _ in scored_tools[:limit]]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        '''
        Internal multi-agent tool partitioning logic.
        '''
        # Simple implementation: evenly distribute tools among agents
        if task_description:
            selected_tools = self._select_for_task(
                task_description, limit=len(self.tools))
        else:
            selected_tools = self.tools

        if overlap:
            # Allow overlap by giving all agents access to all tools
            return [selected_tools for _ in range(num_agents)]
        else:
            # Distribute tools without overlap
            tools_per_agent = len(selected_tools) // num_agents
            remainder = len(selected_tools) % num_agents
            partitions = []
            start = 0
            for i in range(num_agents):
                size = tools_per_agent + (1 if i < remainder else 0)
                partitions.append(selected_tools[start:start + size])
                start += size
            return partitions

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        '''Select tools by their names (case-insensitive).'''
        tool_names = [name.lower() for name in tool_names]
        return [tool for tool in self.tools if tool['name'].lower() in tool_names]

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        '''Filter tools for each role based on name patterns.'''
        result = {}
        for role, patterns in role_patterns.items():
            patterns = [pattern.lower() for pattern in patterns]
            result[role] = [tool for tool in self.tools if any(
                pattern in tool['name'].lower() for pattern in patterns)]
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
        keywords = [keyword.lower() for keyword in keywords]

        def match_tool(tool):
            tool_text = tool['name'].lower() + ' ' + \
                tool.get('description', '').lower()
            if match_all:
                return all(keyword in tool_text for keyword in keywords)
            else:
                return any(keyword in tool_text for keyword in keywords)

        return [tool for tool in self.tools if match_tool(tool)]

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
