from typing import Any, Dict, List, Optional, Union
import re
import math


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
        self.tools = tools or []
        self._name_to_tool = {t.get("name", "").lower(): t for t in self.tools}

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        '''
        Internal single-agent tool selection logic.
        '''
        if not self.tools:
            return []
        # Simple scoring: count keyword matches in name/description
        keywords = [w.lower() for w in re.findall(r"\w+", task_description)]
        scored = []
        for tool in self.tools:
            name = tool.get("name", "").lower()
            desc = tool.get("description", "").lower()
            score = 0
            for kw in keywords:
                if kw in name:
                    score += 2
                if kw in desc:
                    score += 1
            scored.append((score, tool))
        scored.sort(key=lambda x: (-x[0], x[1].get("name", "")))
        # Always return at least 1 tool if available
        result = [t for s, t in scored if s > 0][:limit]
        if not result:
            result = [t for s, t in scored][:limit]
        return result

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        '''
        Internal multi-agent tool partitioning logic.
        '''
        if not self.tools or num_agents < 1:
            return [[] for _ in range(num_agents)]
        tools = self.tools
        if task_description:
            tools = self._select_for_task(
                task_description, limit=len(self.tools))
        if overlap:
            # Each agent gets the same top tools
            return [tools[:] for _ in range(num_agents)]
        else:
            # Partition tools as evenly as possible
            n = len(tools)
            chunk_size = math.ceil(n / num_agents)
            partitions = []
            for i in range(num_agents):
                start = i * chunk_size
                end = min(start + chunk_size, n)
                partitions.append(tools[start:end])
            # If fewer tools than agents, fill with empty lists
            while len(partitions) < num_agents:
                partitions.append([])
            return partitions

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        '''Select tools by their names (case-insensitive).'''
        names = set(n.lower() for n in tool_names)
        return [tool for tool in self.tools if tool.get("name", "").lower() in names]

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        '''Filter tools for each role based on name patterns.'''
        result: Dict[str, List[Any]] = {}
        for role, patterns in role_patterns.items():
            regexes = [re.compile(pat, re.IGNORECASE) for pat in patterns]
            matched = []
            for tool in self.tools:
                name = tool.get("name", "")
                if any(rgx.search(name) for rgx in regexes):
                    matched.append(tool)
            result[role] = matched
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
        if not keywords:
            return self.tools[:]
        kw = [k.lower() for k in keywords]
        result = []
        for tool in self.tools:
            text = (tool.get("name", "") + " " +
                    tool.get("description", "")).lower()
            if match_all:
                if all(k in text for k in kw):
                    result.append(tool)
            else:
                if any(k in text for k in kw):
                    result.append(tool)
        return result

    def select_tools(self, task_description: str, num_agents: Optional[int] = None, overlap: bool = False, limit: int = 5) -> Union[List[Dict[str, Any]], List[List[Dict[str, Any]]]]:
        '''
        Unified public interface for tool selection.
        - Single-agent (num_agents None or <=1): returns a flat list of top tools.
        - Multi-agent (num_agents >1): returns a list of tool lists, one per agent.
        Override this method to implement any custom logic.
        '''
        if not num_agents or num_agents <= 1:
            return self._select_for_task(task_description, limit=limit)
        else:
            return self._partition_tools_for_multi_agent(num_agents, overlap=overlap, task_description=task_description)
