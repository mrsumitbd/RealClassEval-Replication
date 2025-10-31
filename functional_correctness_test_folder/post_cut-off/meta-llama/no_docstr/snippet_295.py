
from typing import List, Dict, Any, Optional


class ToolSelector:

    def __init__(self, tools: List[Dict[str, Any]]):
        """
        Initialize the ToolSelector with a list of tools.

        Args:
        tools (List[Dict[str, Any]]): A list of dictionaries where each dictionary represents a tool.
        """
        self.tools = tools

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Select tools relevant to a task description.

        Args:
        task_description (str): A description of the task.
        limit (int): The maximum number of tools to return. Defaults to 5.

        Returns:
        List[Dict[str, Any]]: A list of tools relevant to the task.
        """
        # For simplicity, this example assumes that the task description is matched against the tool's 'description' key.
        # In a real-world scenario, you might want to use a more sophisticated method such as NLP or embeddings.
        relevant_tools = sorted(self.tools, key=lambda tool: task_description.lower(
        ) in tool.get('description', '').lower(), reverse=True)
        return relevant_tools[:limit]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        """
        Partition the selected tools among multiple agents.

        Args:
        num_agents (int): The number of agents.
        overlap (bool): Whether to allow overlap between the tools assigned to different agents. Defaults to False.
        task_description (Optional[str]): If provided, select tools relevant to this task before partitioning. Defaults to None.

        Returns:
        List[List[Dict[str, Any]]]: A list of lists where each inner list contains the tools assigned to an agent.
        """
        if task_description:
            selected_tools = self._select_for_task(task_description)
        else:
            selected_tools = self.tools

        if overlap:
            # If overlap is allowed, simply divide the tools into num_agents lists.
            # Tools are distributed as evenly as possible.
            base_size, remainder = divmod(len(selected_tools), num_agents)
            partitions = []
            start = 0
            for i in range(num_agents):
                size = base_size + (1 if i < remainder else 0)
                partitions.append(selected_tools[start:start + size])
                start += size
            return partitions
        else:
            # If overlap is not allowed, ensure that each tool is assigned to exactly one agent.
            return [selected_tools[i::num_agents] for i in range(num_agents)]

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        """
        Select tools by their names.

        Args:
        tool_names (List[str]): A list of tool names.

        Returns:
        List[Any]: A list of tools whose names match the provided names.
        """
        return [tool for tool in self.tools if tool['name'] in tool_names]

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        """
        Filter tools based on their roles.

        Args:
        role_patterns (Dict[str, List[str]]): A dictionary where keys are role names and values are lists of patterns to match.

        Returns:
        Dict[str, List[Any]]: A dictionary where keys are role names and values are lists of tools that match the corresponding patterns.
        """
        result = {}
        for role, patterns in role_patterns.items():
            result[role] = [tool for tool in self.tools if any(pattern.lower() in tool.get(
                'description', '').lower() or pattern.lower() in tool.get('name', '').lower() for pattern in patterns)]
        return result

    def filter_by_keywords(self, keywords: List[str], match_all: bool = False) -> List[Any]:
        """
        Filter tools based on keywords.

        Args:
        keywords (List[str]): A list of keywords.
        match_all (bool): Whether to match all keywords or any of them. Defaults to False.

        Returns:
        List[Any]: A list of tools that match the keywords according to the match_all parameter.
        """
        if match_all:
            return [tool for tool in self.tools if all(keyword.lower() in tool.get('description', '').lower() or keyword.lower() in tool.get('name', '').lower() for keyword in keywords)]
        else:
            return [tool for tool in self.tools if any(keyword.lower() in tool.get('description', '').lower() or keyword.lower() in tool.get('name', '').lower() for keyword in keywords)]

    def select_tools(self, task_description: str, num_agents: Optional[int] = None, overlap: bool = False, limit: int = 5) -> Any:
        """
        Select tools for a task and optionally partition them among multiple agents.

        Args:
        task_description (str): A description of the task.
        num_agents (Optional[int]): The number of agents. If None, tools are not partitioned. Defaults to None.
        overlap (bool): Whether to allow overlap between the tools assigned to different agents. Defaults to False.
        limit (int): The maximum number of tools to return or partition. Defaults to 5.

        Returns:
        Any: If num_agents is None, returns a list of selected tools. Otherwise, returns a list of lists where each inner list contains the tools assigned to an agent.
        """
        selected_tools = self._select_for_task(task_description, limit)
        if num_agents is None:
            return selected_tools
        else:
            # task_description is already used in _select_for_task
            return self._partition_tools_for_multi_agent(num_agents, overlap, task_description=None)


# Example usage:
if __name__ == "__main__":
    tools = [
        {'name': 'Tool1', 'description': 'This is tool1'},
        {'name': 'Tool2', 'description': 'This is tool2'},
        {'name': 'Tool3', 'description': 'This is tool3 for taskA'},
        {'name': 'Tool4', 'description': 'This is tool4 for taskB'},
    ]

    selector = ToolSelector(tools)

    print(selector.select_by_names(['Tool1', 'Tool3']))
    print(selector.filter_by_roles({'role1': ['taskA']}))
    print(selector.filter_by_keywords(['taskA'], match_all=True))
    print(selector.select_tools('taskA', num_agents=2, overlap=True))
