
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
import re
import math


class ToolSelector:
    """
    Primary interface for tool selection across single-agent and multi-agent scenarios.
    Use `select_tools(task_description, num_agents=None, overlap=False, limit=5)` to pick or partition tools.
    Override `select_tools` to implement custom selection strategies.
    """

    _WORD_RE = re.compile(r"\w+")

    def __init__(self, tools: List[Dict[str, Any]]):
        """
        Initialize with available tools.
        Args:
            tools: List of tool definitions from ToolManager
        """
        self.tools: List[Dict[str, Any]] = tools
        # Build a name lookup (case-insensitive)
        self._name_index: Dict[str, Dict[str, Any]] = {
            tool.get("name", "").lower(): tool for tool in tools if "name" in tool
        }

    def _tokenize(self, text: str) -> List[str]:
        return [m.group(0).lower() for m in self._WORD_RE.finditer(text or "")]

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Internal single-agent tool selection logic.
        """
        task_tokens = set(self._tokenize(task_description))
        scored: List[Tuple[int, Dict[str, Any]]] = []

        for tool in self.tools:
            name = tool.get("name", "")
            desc = tool.get("description", "")
            name_tokens = set(self._tokenize(name))
            desc_tokens = set(self._tokenize(desc))

            # Simple scoring: name matches weighted more heavily
            name_score = len(task_tokens & name_tokens)
            desc_score = len(task_tokens & desc_tokens)
            score = name_score * 2 + desc_score

            scored.append((score, tool))

        # Sort by score descending, then by name ascending
        scored.sort(key=lambda x: (-x[0], x[1].get("name", "").lower()))
        return [tool for _, tool in scored[:limit]]

    def _partition_tools_for_multi_agent(
        self,
        num_agents: int,
        overlap: bool = False,
        task_description: Optional[str] = None,
    ) -> List[List[Dict[str, Any]]]:
        """
        Internal multi-agent tool partitioning logic.
        """
        if num_agents <= 0:
            raise ValueError("num_agents must be >= 1")

        # If a task description is provided, first select top tools
        if task_description:
            selected = self._select_for_task(
                task_description, limit=len(self.tools))
        else:
            selected = list(self.tools)

        if overlap:
            # Each agent gets the full set
            return [list(selected) for _ in range(num_agents)]

        # Evenly split the selected tools
        n = len(selected)
        chunk_size = math.ceil(n / num_agents)
        partitions: List[List[Dict[str, Any]]] = []
        for i in range(num_agents):
            start = i * chunk_size
            end = start + chunk_size
            partitions.append(selected[start:end])
        return partitions

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        """Select tools by their names (case-insensitive)."""
        result: List[Any] = []
        for name in tool_names:
            tool = self._name_index.get(name.lower())
            if tool:
                result.append(tool)
        return result

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        """
        Filter tools for each role based on name patterns.
        """
        role_to_tools: Dict[str, List[Any]] = {}
        for role, patterns in role_patterns.items():
            compiled = [re.compile(p, re.IGNORECASE) for p in patterns]
            matched = [
                tool
                for tool in self.tools
                if any(c.search(tool.get("name", "")) for c in compiled)
            ]
            role_to_tools[role] = matched
        return role_to_tools

    def filter_by_keywords(
        self, keywords: List[str], match_all: bool = False
    ) -> List[Any]:
        """
        Filter tools that match specified keywords in name or description.
        Args:
            keywords: List of keywords to match
            match_all: If True, tools must match all keywords. If False, match any keyword.
        Returns:
            List of tools matching the criteria
        """
        if not keywords:
            return list(self.tools)

        lower_keywords = [kw.lower() for kw in keywords]
        matched: List[Any] = []

        for tool in self.tools:
            text = f"{tool.get('name', '')} {tool.get('description', '')}".lower()
            if match_all:
                if all(kw in text for kw in lower_keywords):
                    matched.append(tool)
            else:
                if any(kw in text for kw in lower_keywords):
                    matched.append(tool)

        return matched

    def select_tools(
        self,
        task_description: str,
        num_agents: Optional[int] = None,
        overlap: bool = False,
        limit: int = 5,
    ) -> Any:
        """
        Unified public interface for tool selection.
        - Single-agent (num_agents None or <=1): returns a flat list of top tools.
        - Multi-agent (num_agents >1): returns a list of tool lists, one per agent.
        Override this method to implement any custom logic.
        """
        if num_agents is None or num_agents <= 1:
            return self._select_for_task(task_description, limit=limit)
        else:
            return self._partition_tools_for_multi_agent(
                num_agents=num_agents, overlap=overlap, task_description=task_description
            )
