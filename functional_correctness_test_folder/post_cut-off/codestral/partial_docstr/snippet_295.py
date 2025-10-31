
from typing import List, Dict, Any, Optional
import re


class ToolSelector:

    def __init__(self, tools: List[Dict[str, Any]]):
        self.tools = tools

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        # Implement task-based selection logic here
        # For now, return the first 'limit' tools as a placeholder
        return self.tools[:limit]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        # Implement multi-agent partitioning logic here
        # For now, distribute tools evenly among agents
        if overlap:
            # If overlap is True, each agent gets all tools
            return [self.tools for _ in range(num_agents)]
        else:
            # If overlap is False, distribute tools evenly
            avg = len(self.tools) // num_agents
            remainder = len(self.tools) % num_agents
            partitions = []
            start = 0
            for i in range(num_agents):
                end = start + avg + (1 if i < remainder else 0)
                partitions.append(self.tools[start:end])
                start = end
            return partitions

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        selected_tools = []
        for tool in self.tools:
            if tool['name'].lower() in [name.lower() for name in tool_names]:
                selected_tools.append(tool)
        return selected_tools

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        filtered_tools = {role: [] for role in role_patterns}
        for tool in self.tools:
            for role, patterns in role_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, tool['name'], re.IGNORECASE):
                        filtered_tools[role].append(tool)
                        break
        return filtered_tools

    def filter_by_keywords(self, keywords: List[str], match_all: bool = False) -> List[Any]:
        filtered_tools = []
        for tool in self.tools:
            if match_all:
                if all(keyword.lower() in tool['name'].lower() for keyword in keywords):
                    filtered_tools.append(tool)
            else:
                if any(keyword.lower() in tool['name'].lower() for keyword in keywords):
                    filtered_tools.append(tool)
        return filtered_tools

    def select_tools(self, task_description: str, num_agents: Optional[int] = None, overlap: bool = False, limit: int = 5) -> Any:
        if num_agents is None or num_agents <= 1:
            return self._select_for_task(task_description, limit)
        else:
            return self._partition_tools_for_multi_agent(num_agents, overlap, task_description)
