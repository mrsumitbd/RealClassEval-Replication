
from typing import List, Dict, Any, Optional
import re


class ToolSelector:

    def __init__(self, tools: List[Dict[str, Any]]):
        '''
        Initialize with available tools.
        Args:
            tools: List of tool definitions from ToolManager
        '''
        self.tools = tools or []
        # Normalize tool names for case-insensitive lookup
        self._name_to_tool = {
            t['name'].lower(): t for t in self.tools if 'name' in t}

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        # Select tools whose name or description matches the task_description keywords
        if not task_description:
            return self.tools[:limit]
        keywords = re.findall(r'\w+', task_description.lower())
        scored = []
        for tool in self.tools:
            score = 0
            name = tool.get('name', '').lower()
            desc = tool.get('description', '').lower()
            for kw in keywords:
                if kw in name:
                    score += 2
                if kw in desc:
                    score += 1
            if score > 0:
                scored.append((score, tool))
        scored.sort(reverse=True, key=lambda x: x[0])
        return [t for _, t in scored[:limit]] if scored else self.tools[:limit]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        # Optionally filter tools for the task
        if task_description:
            tools = self._select_for_task(
                task_description, limit=len(self.tools))
        else:
            tools = self.tools[:]
        n = len(tools)
        if num_agents <= 0:
            return []
        if n == 0:
            return [[] for _ in range(num_agents)]
        if overlap:
            # Each agent gets the same set (all tools)
            return [tools[:] for _ in range(num_agents)]
        else:
            # Partition tools as evenly as possible
            partitions = [[] for _ in range(num_agents)]
            for idx, tool in enumerate(tools):
                partitions[idx % num_agents].append(tool)
            return partitions

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        '''Select tools by their names (case-insensitive).'''
        result = []
        names_lower = set(n.lower() for n in tool_names)
        for t in self.tools:
            if t.get('name', '').lower() in names_lower:
                result.append(t)
        return result

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        # role_patterns: {role: [pattern1, pattern2, ...]}
        result = {}
        for role, patterns in role_patterns.items():
            matched = []
            for tool in self.tools:
                tool_roles = tool.get('roles', [])
                if not isinstance(tool_roles, list):
                    tool_roles = [tool_roles]
                for pat in patterns:
                    pat_re = re.compile(pat, re.IGNORECASE)
                    if any(pat_re.search(str(r)) for r in tool_roles):
                        matched.append(tool)
                        break
            result[role] = matched
        return result

    def filter_by_keywords(self, keywords: List[str], match_all: bool = False) -> List[Any]:
        # Search in name and description
        if not keywords:
            return self.tools[:]
        keywords = [k.lower() for k in keywords]
        result = []
        for tool in self.tools:
            text = (tool.get('name', '') + ' ' +
                    tool.get('description', '')).lower()
            if match_all:
                if all(kw in text for kw in keywords):
                    result.append(tool)
            else:
                if any(kw in text for kw in keywords):
                    result.append(tool)
        return result

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
