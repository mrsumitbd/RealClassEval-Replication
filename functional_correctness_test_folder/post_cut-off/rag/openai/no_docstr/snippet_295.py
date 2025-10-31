
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
import fnmatch
import re


class ToolSelector:
    """
    Primary interface for tool selection across single-agent and multi-agent scenarios.
    Use `select_tools(task_description, num_agents=None, overlap=False, limit=5)` to pick or partition tools.
    Override `select_tools` to implement custom selection strategies.
    """

    def __init__(self, tools: List[Dict[str, Any]]):
        """
        Initialize with available tools.
        Args:
            tools: List of tool definitions from ToolManager
        """
        self.tools: List[Dict[str, Any]] = tools
        # Build a name lookup for quick access
        self._name_lookup: Dict[str, Dict[str, Any]] = {
            tool.get("name", "").lower(): tool for tool in tools
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _score_tool(self, tool: Dict[str, Any], keywords: List[str]) -> int:
        """
        Compute a simple relevance score for a tool based on keyword matches
        in its name and description.
        """
        name = tool.get("name", "").lower()
        desc = tool.get("description", "").lower()
        score = 0
        for kw in keywords:
            kw_l = kw.lower()
            if kw_l in name or kw_l in desc:
                score += 1
        return score

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Internal single-agent tool selection logic.
        """
        # Extract simple keywords from task description
        # For simplicity, split on whitespace and strip punctuation
        words = re.findall(r"\b\w+\b", task_description.lower())
        # Remove common stopwords
        stopwords = {"the", "and", "or", "to", "in",
                     "of", "a", "an", "with", "for", "on", "by"}
        keywords = [w for w in words if w not in stopwords]

        # Score each tool
        scored = []
        for tool in self.tools:
            score = self._score_tool(tool, keywords)
            if score > 0:
                scored.append((score, tool))

        # Sort by score descending, then by name
        scored.sort(key=lambda x: (-x[0], x[1].get("name", "").lower()))

        # Return top `limit` tools
        return [t for _, t in scored[:limit]]

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
            raise ValueError("num_agents must be a positive integer")

        # If a task description is provided, we can optionally filter tools first
        # For simplicity, we ignore task_description here and use all tools
        tools_to_use = self.tools

        if overlap:
            # Each agent gets the full set of tools
            return [list(tools_to_use) for _ in range(num_agents)]

        # Round-robin assignment
        partitions: List[List[Dict[str, Any]]] = [[]
                                                  for _ in range(num_agents)]
        for idx, tool in enumerate(tools_to_use):
            agent_idx = idx % num_agents
            partitions[agent_idx].append(tool)

        return partitions

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        """Select tools by their names (case-insensitive)."""
        names_set = {name.lower() for name in tool_names}
        selected = [tool for name, tool in self._name_lookup.items()
                    if name in names_set]
        return selected

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        """
        Filter tools for each role based on name patterns.
        role_patterns: mapping from role name to list of glob patterns.
        """
        result: Dict[str, List[Any]] = {}
        for role, patterns in role_patterns.items():
            matched = []
            for tool in self.tools:
                name = tool.get("name", "")
                if any(fnmatch.fnmatchcase(name, pat) for pat in patterns):
                    matched.append(tool)
            result[role] = matched
        return result

    def filter_by_keywords(
        self, keywords: List[str], match_all: bool = False
    ) -> List[Any]:
        """
        Filter tools that match specified keywords in name or description.
        """
        matched: List[Any] = []
        for tool in self.tools:
            name = tool.get("name", "").lower()
            desc = tool.get("description", "").lower()
            matches = [kw.lower() in name or kw.lower()
                       in desc for kw in keywords]
            if match_all:
                if all(matches):
                    matched.append(tool)
            else:
                if any(matches):
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
