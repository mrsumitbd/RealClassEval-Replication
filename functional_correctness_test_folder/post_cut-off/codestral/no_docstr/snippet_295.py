
from typing import List, Dict, Any, Optional
import re


class ToolSelector:

    def __init__(self, tools: List[Dict[str, Any]]):
        self.tools = tools

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        selected_tools = []
        for tool in self.tools:
            if any(keyword.lower() in task_description.lower() for keyword in tool.get('keywords', [])):
                selected_tools.append(tool)
        return selected_tools[:limit]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        if task_description:
            selected_tools = self._select_for_task(task_description)
        else:
            selected_tools = self.tools

        if overlap:
            return [selected_tools for _ in range(num_agents)]

        partition_size = len(selected_tools) // num_agents
        partitions = []
        for i in range(num_agents):
            start = i * partition_size
            end = (i + 1) * partition_size if i != num_agents - \
                1 else len(selected_tools)
            partitions.append(selected_tools[start:end])
        return partitions

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        return [tool for tool in self.tools if tool['name'] in tool_names]

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        filtered_tools = {}
        for role, patterns in role_patterns.items():
            filtered_tools[role] = []
            for tool in self.tools:
                if any(re.search(pattern, tool['name']) for pattern in patterns):
                    filtered_tools[role].append(tool)
        return filtered_tools

    def filter_by_keywords(self, keywords: List[str], match_all: bool = False) -> List[Any]:
        if match_all:
            return [tool for tool in self.tools if all(keyword.lower() in [kw.lower() for kw in tool.get('keywords', [])] for keyword in keywords)]
        else:
            return [tool for tool in self.tools if any(keyword.lower() in [kw.lower() for kw in tool.get('keywords', [])] for keyword in keywords)]

    def select_tools(self, task_description: str, num_agents: Optional[int] = None, overlap: bool = False, limit: int = 5) -> Any:
        if num_agents:
            return self._partition_tools_for_multi_agent(num_agents, overlap, task_description)
        else:
            return self._select_for_task(task_description, limit)
