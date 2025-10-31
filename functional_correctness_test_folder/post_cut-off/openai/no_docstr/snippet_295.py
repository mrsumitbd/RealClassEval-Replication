
from typing import List, Dict, Any, Optional
import re
import math


class ToolSelector:
    """
    A simple tool selector that can filter and partition a list of tools
    based on names, roles, keywords, and task descriptions.
    """

    def __init__(self, tools: List[Dict[str, Any]]):
        """
        Parameters
        ----------
        tools : List[Dict[str, Any]]
            A list of tool dictionaries. Each dictionary may contain the
            following keys:
                - name (str): The unique name of the tool.
                - role (str): The role or category of the tool.
                - description (str): A textual description of the tool.
                - keywords (List[str]): A list of keywords associated with the tool.
        """
        self.tools = tools

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------
    def _tokenize(self, text: str) -> List[str]:
        """Return a list of lower‑cased words from the given text."""
        return re.findall(r"\b\w+\b", text.lower())

    def _score_tool(self, tool: Dict[str, Any], tokens: List[str]) -> int:
        """Return a relevance score for a tool based on token overlap."""
        description = tool.get("description", "")
        desc_tokens = set(self._tokenize(description))
        return len(set(tokens) & desc_tokens)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Return the top `limit` tools that best match the task description.
        """
        tokens = self._tokenize(task_description)
        scored = [(self._score_tool(t, tokens), t) for t in self.tools]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [t for _, t in scored[:limit] if _[0] > 0]

    def _partition_tools_for_multi_agent(
        self,
        num_agents: int,
        overlap: bool = False,
        task_description: Optional[str] = None,
    ) -> List[List[Dict[str, Any]]]:
        """
        Partition the tools into `num_agents` groups. If `overlap` is True,
        each group will share a common set of tools (the top tools for the
        task). If `task_description` is provided, the top tools are used
        as the overlapping set.
        """
        if num_agents <= 0:
            raise ValueError("num_agents must be a positive integer")

        # Determine the overlapping set
        overlap_set = []
        if overlap and task_description:
            overlap_set = self._select_for_task(task_description, limit=5)

        # Remaining tools after removing overlap
        remaining = [t for t in self.tools if t not in overlap_set]

        # Distribute remaining tools round‑robin
        groups = [[] for _ in range(num_agents)]
        for idx, tool in enumerate(remaining):
            groups[idx % num_agents].append(tool)

        # Prepend overlap set to each group
        if overlap_set:
            groups = [[*overlap_set, *g] for g in groups]

        return groups

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        """
        Return the tools whose names are in `tool_names`.
        """
        name_set = set(tool_names)
        return [t for t in self.tools if t.get("name") in name_set]

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        """
        Return a dictionary mapping each role to the list of tools that
        match any of the regex patterns for that role.
        """
        result: Dict[str, List[Any]] = {}
        for role, patterns in role_patterns.items():
            compiled = [re.compile(p, re.IGNORECASE) for p in patterns]
            matched = [
                t
                for t in self.tools
                if any(c.search(t.get("role", "")) for c in compiled)
            ]
            result[role] = matched
        return result

    def filter_by_keywords(self, keywords: List[str], match_all: bool = False) -> List[Any]:
        """
        Return tools that contain the given keywords. If `match_all` is True,
        a tool must contain all keywords; otherwise any keyword suffices.
        """
        kw_set = set(k.lower() for k in keywords)
        matched = []
        for t in self.tools:
            tool_kw = set(k.lower() for k in t.get("keywords", []))
            if match_all:
                if kw_set.issubset(tool_kw):
                    matched.append(t)
            else:
                if kw_set & tool_kw:
                    matched.append(t)
        return matched

    def select_tools(
        self,
        task_description: str,
        num_agents: Optional[int] = None,
        overlap: bool = False,
        limit: int = 5,
    ) -> Any:
        """
        Main entry point. If `num_agents` is provided, partition the tools
        for a multi‑agent scenario; otherwise return the top tools for the
        task.
        """
        if num_agents is None:
            return self._select_for_task(task_description, limit=limit)
        else:
            return self._partition_tools_for_multi_agent(
                num_agents=num_agents, overlap=overlap, task_description=task_description
            )
