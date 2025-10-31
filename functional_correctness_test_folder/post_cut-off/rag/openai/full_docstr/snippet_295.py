
import re
from typing import Any, Dict, List, Optional, Tuple, Union


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
        # Store a copy to avoid accidental mutation
        self.tools = [dict(t) for t in tools]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Return a list of lower‑cased word tokens from a string."""
        return re.findall(r'\w+', text.lower())

    def _score_tool(self, tool: Dict[str, Any], tokens: List[str]) -> int:
        """Score a tool by counting how many task tokens appear in its name or description."""
        name = tool.get('name', '')
        desc = tool.get('description', '')
        content = f'{name} {desc}'.lower()
        return sum(1 for t in tokens if t in content)

    # ------------------------------------------------------------------
    # Single‑agent selection
    # ------------------------------------------------------------------
    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        '''
        Internal single-agent tool selection logic.
        '''
        if not task_description:
            # If no description, return the first `limit` tools
            return self.tools[:limit]

        tokens = self._tokenize(task_description)
        scored = [(self._score_tool(t, tokens), t) for t in self.tools]
        # Sort by score descending, then by name ascending for stability
        scored.sort(key=lambda x: (-x[0], x[1].get('name', '').lower()))
        # Filter out tools with zero score unless we have fewer than limit
        selected = [t for score, t in scored if score > 0]
        if len(selected) < limit:
            # Add remaining tools sorted by name
            remaining = [t for score, t in scored if score == 0]
            remaining.sort(key=lambda t: t.get('name', '').lower())
            selected.extend(remaining)
        return selected[:limit]

    # ------------------------------------------------------------------
    # Multi‑agent partitioning
    # ------------------------------------------------------------------
    def _partition_tools_for_multi_agent(
        self,
        num_agents: int,
        overlap: bool = False,
        task_description: Optional[str] = None,
    ) -> List[List[Dict[str, Any]]]:
        '''
        Internal multi-agent tool partitioning logic.
        '''
        if num_agents <= 1:
            raise ValueError(
                "num_agents must be > 1 for multi-agent partitioning")

        # First, sort tools by relevance to the task (if provided)
        if task_description:
            sorted_tools = self._select_for_task(
                task_description, limit=len(self.tools))
        else:
            # If no task description, just sort by name
            sorted_tools = sorted(
                self.tools, key=lambda t: t.get('name', '').lower())

        if overlap:
            # Each agent gets the same top tools
            return [sorted_tools[:] for _ in range(num_agents)]

        # Disjoint partition: round‑robin distribution
        partitions: List[List[Dict[str, Any]]] = [[]
                                                  for _ in range(num_agents)]
        for idx, tool in enumerate(sorted_tools):
            partitions[idx % num_agents].append(tool)
        return partitions

    # ------------------------------------------------------------------
    # Public convenience methods
    # ------------------------------------------------------------------
    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        '''Select tools by their names (case-insensitive).'''
        names_lower = {n.lower() for n in tool_names}
        return [t for t in self.tools if t.get('name', '').lower() in names_lower]

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        '''Filter tools for each role based on name patterns.'''
        result: Dict[str, List[Any]] = {}
        for role, patterns in role_patterns.items():
            compiled = [re.compile(p, re.IGNORECASE) for p in patterns]
            matched = [
                t for t in self.tools
                if any(c.search(t.get('name', '')) for c in compiled)
            ]
            result[role] = matched
        return result

    def filter_by_keywords(
        self,
        keywords: List[str],
        match_all: bool = False,
    ) -> List[Any]:
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

        keywords_lower = [k.lower() for k in keywords]
        matched: List[Any] = []
        for t in self.tools:
            content = f"{t.get('name', '')} {t.get('description', '')}".lower()
            if match_all:
                if all(k in content for k in keywords_lower):
                    matched.append(t)
            else:
                if any(k in content for k in keywords_lower):
                    matched.append(t)
        return matched

    # ------------------------------------------------------------------
    # Unified public interface
    # ------------------------------------------------------------------
    def select_tools(
        self,
        task_description: str,
        num_agents: Optional[int] = None,
        overlap: bool = False,
        limit: int = 5,
    ) -> Union[List[Dict[str, Any]], List[List[Dict[str, Any]]]]:
        '''
        Unified public interface for tool selection.
        - Single-agent (num_agents None or <=1): returns a flat list of top tools.
        - Multi-agent (num_agents >1): returns a list of tool lists, one per agent.
        Override this method to implement any custom logic.
        '''
        if num_agents is None or num_agents <= 1:
            return self._select_for_task(task_description, limit=limit)

        # Multi‑agent
        partitions = self._partition_tools_for_multi_agent(
            num_agents=num_agents,
            overlap=overlap,
            task_description=task_description,
        )
        # If a limit is specified, trim each partition
        if limit is not None:
            partitions = [p[:limit] for p in partitions]
        return partitions
