
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
        # Here, we just return the first `limit` tools that contain the task_description in their name or description
        return [tool for tool in self.tools if task_description.lower() in tool.get('name', '').lower() or task_description.lower() in tool.get('description', '').lower()][:limit]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        '''
        Internal multi-agent tool partitioning logic.
        '''
        # Placeholder for actual partitioning logic
        # Here, we simply divide the tools among agents
        selected_tools = self._select_for_task(
            task_description) if task_description else self.tools
        if overlap:
            return [selected_tools for _ in range(num_agents)]
        else:
            partition_size = math.ceil(len(selected_tools) / num_agents)
            return [selected_tools[i * partition_size:(i + 1) * partition_size] for i in range(num_agents)]

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        '''Select tools by their names (case-insensitive).'''
        return [tool for tool in self.tools if tool.get('name', '').lower() in (name.lower() for name in tool_names)]

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        '''Filter tools for each role based on name patterns.'''
        filtered_tools = {}
        for role, patterns in role_patterns.items():
            filtered_tools[role] = [tool for tool in self.tools if any(
                pattern.lower() in tool.get('name', '').lower() for pattern in patterns)]
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
        if match_all:
            return [tool for tool in self.tools if all(keyword.lower() in tool.get('name', '').lower() or keyword.lower() in tool.get('description', '').lower() for keyword in keywords)]
        else:
            return [tool for tool in self.tools if any(keyword.lower() in tool.get('name', '').lower() or keyword.lower() in tool.get('description', '').lower() for keyword in keywords)]

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
