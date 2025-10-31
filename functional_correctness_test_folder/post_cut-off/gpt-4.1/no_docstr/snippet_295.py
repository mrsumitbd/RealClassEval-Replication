
from typing import List, Dict, Any, Optional
import re


class ToolSelector:

    def __init__(self, tools: List[Dict[str, Any]]):
        self.tools = tools

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        # Simple keyword matching in tool 'description' or 'name'
        task_keywords = set(re.findall(r'\w+', task_description.lower()))

        def score(tool):
            text = (tool.get('description', '') +
                    ' ' + tool.get('name', '')).lower()
            tool_words = set(re.findall(r'\w+', text))
            return len(task_keywords & tool_words)
        scored_tools = sorted(self.tools, key=score, reverse=True)
        return [tool for tool in scored_tools if score(tool) > 0][:limit] or scored_tools[:limit]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        if task_description:
            selected_tools = self._select_for_task(
                task_description, limit=len(self.tools))
        else:
            selected_tools = self.tools[:]
        n = len(selected_tools)
        if num_agents <= 0:
            return []
        if overlap:
            return [selected_tools[:] for _ in range(num_agents)]
        else:
            partitions = [[] for _ in range(num_agents)]
            for idx, tool in enumerate(selected_tools):
                partitions[idx % num_agents].append(tool)
            return partitions

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        name_set = set(name.lower() for name in tool_names)
        return [tool for tool in self.tools if tool.get('name', '').lower() in name_set]

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        result = {}
        for role, patterns in role_patterns.items():
            compiled_patterns = [re.compile(
                pat, re.IGNORECASE) for pat in patterns]
            matched_tools = []
            for tool in self.tools:
                tool_roles = tool.get('roles', [])
                if any(any(pat.search(r) for pat in compiled_patterns) for r in tool_roles):
                    matched_tools.append(tool)
            result[role] = matched_tools
        return result

    def filter_by_keywords(self, keywords: List[str], match_all: bool = False) -> List[Any]:
        keywords = [kw.lower() for kw in keywords]
        result = []
        for tool in self.tools:
            text = (tool.get('description', '') +
                    ' ' + tool.get('name', '')).lower()
            if match_all:
                if all(kw in text for kw in keywords):
                    result.append(tool)
            else:
                if any(kw in text for kw in keywords):
                    result.append(tool)
        return result

    def select_tools(self, task_description: str, num_agents: Optional[int] = None, overlap: bool = False, limit: int = 5) -> Any:
        if num_agents is None or num_agents <= 1:
            return self._select_for_task(task_description, limit=limit)
        else:
            return self._partition_tools_for_multi_agent(num_agents, overlap=overlap, task_description=task_description)
