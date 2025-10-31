
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
        self.tools = tools or []

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        '''
        Internal single-agent tool selection logic.
        '''
        if not task_description:
            return self.tools[:limit]
        # Simple keyword matching in name or description
        keywords = re.findall(r'\w+', task_description.lower())
        scored_tools = []
        for tool in self.tools:
            score = 0
            name = tool.get('name', '').lower()
            desc = tool.get('description', '').lower()
            for kw in keywords:
                if kw in name or kw in desc:
                    score += 1
            scored_tools.append((score, tool))
        scored_tools.sort(key=lambda x: (-x[0], self.tools.index(x[1])))
        selected = [tool for score, tool in scored_tools if score > 0]
        if len(selected) < limit:
            # Fill up with remaining tools if not enough matches
            remaining = [t for t in self.tools if t not in selected]
            selected += remaining[:limit - len(selected)]
        return selected[:limit]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        '''
        Internal multi-agent tool partitioning logic.
        '''
        if num_agents <= 1:
            return [self._select_for_task(task_description or "", limit=len(self.tools))]
        selected_tools = self._select_for_task(
            task_description or "", limit=len(self.tools))
        if overlap:
            # Each agent gets the same set
            return [selected_tools[:] for _ in range(num_agents)]
        else:
            # Partition tools as evenly as possible
            partitions = [[] for _ in range(num_agents)]
            for idx, tool in enumerate(selected_tools):
                partitions[idx % num_agents].append(tool)
            return partitions

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        '''Select tools by their names (case-insensitive).'''
        name_set = set(n.lower() for n in tool_names)
        return [tool for tool in self.tools if tool.get('name', '').lower() in name_set]

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        '''Filter tools for each role based on name patterns.'''
        result = {}
        for role, patterns in role_patterns.items():
            compiled_patterns = [re.compile(
                pat, re.IGNORECASE) for pat in patterns]
            matched = []
            for tool in self.tools:
                name = tool.get('name', '')
                if any(pat.search(name) for pat in compiled_patterns):
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
        keywords = [kw.lower() for kw in keywords]
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
            # For multi-agent, partition only up to the limit
            selected_tools = self._select_for_task(
                task_description, limit=limit * num_agents)
            if overlap:
                return [selected_tools[:limit] for _ in range(num_agents)]
            else:
                partitions = [[] for _ in range(num_agents)]
                for idx, tool in enumerate(selected_tools):
                    if len(partitions[idx % num_agents]) < limit:
                        partitions[idx % num_agents].append(tool)
                return partitions
