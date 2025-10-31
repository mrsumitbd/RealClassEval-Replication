
from typing import List, Dict, Any, Optional
import re
import math


class ToolSelector:
    def __init__(self, tools: List[Dict[str, Any]]):
        """
        Initialize with available tools.
        Args:
            tools: List of tool definitions from ToolManager
        """
        self.tools = tools

    def _score_tool(self, tool: Dict[str, Any], task_description: str) -> int:
        """
        Compute a simple relevance score for a tool based on keyword matches.
        """
        score = 0
        keywords = tool.get("keywords", [])
        if not isinstance(keywords, list):
            keywords = [keywords]
        for kw in keywords:
            if kw and re.search(rf"\b{re.escape(kw.lower())}\b", task_description.lower()):
                score += 1
        # Also give a small bonus if the tool name appears in the description
        name = tool.get("name", "")
        if name and re.search(rf"\b{re.escape(name.lower())}\b", task_description.lower()):
            score += 1
        return score

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Return the top `limit` tools most relevant to the task description.
        """
        scored = [
            (self._score_tool(tool, task_description), tool)
            for tool in self.tools
        ]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [tool for _, tool in scored[:limit]]

    def _partition_tools_for_multi_agent(
        self,
        num_agents: int,
        overlap: bool = False,
        task_description: Optional[str] = None,
    ) -> List[List[Dict[str, Any]]]:
        """
        Partition tools among multiple agents.
        """
        if overlap:
            # All agents get the same list of tools
            return [self.tools[:] for _ in range(num_agents)]

        # Determine the number of tools to consider
        # If a task description is provided, rank tools by relevance first
        if task_description:
            ranked = sorted(
                self.tools,
                key=lambda t: self._score_tool(t, task_description),
                reverse=True,
            )
        else:
            ranked = self.tools[:]

        # Split into roughly equal chunks
        chunk_size = math.ceil(len(ranked) / num_agents)
        partitions = [
            ranked[i * chunk_size: (i + 1) * chunk_size] for i in range(num_agents)
        ]
        return partitions

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        """
        Select tools by their names (case-insensitive).
        """
        names_lower = {name.lower() for name in tool_names}
        return [tool for tool in self.tools if tool.get("name", "").lower() in names_lower]

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        """
        Filter tools by role patterns.
        """
        result: Dict[str, List[Any]] = {}
        for role, patterns in role_patterns.items():
            matched = []
            for tool in self.tools:
                tool_role = tool.get("role", "")
                if not isinstance(tool_role, str):
                    continue
                for pat in patterns:
                    if pat.lower() in tool_role.lower():
                        matched.append(tool)
                        break
            result[role] = matched
        return result

    def filter_by_keywords(self, keywords: List[str], match_all: bool = False) -> List[Any]:
        """
        Filter tools that contain the given keywords.
        """
        keywords_lower = {kw.lower() for kw in keywords}
        matched_tools = []
        for tool in self.tools:
            tool_keywords = tool.get("keywords", [])
            if not isinstance(tool_keywords, list):
                tool_keywords = [tool_keywords]
            tool_keywords_lower = {kw.lower() for kw in tool_keywords if kw}
            if match_all:
                if keywords_lower.issubset(tool_keywords_lower):
                    matched_tools.append(tool)
            else:
                if keywords_lower & tool_keywords_lower:
                    matched_tools.append(tool)
        return matched_tools

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
        if not num_agents or num_agents <= 1:
            return self._select_for_task(task_description, limit=limit)

        # Multi-agent case
        partitions = self._partition_tools_for_multi_agent(
            num_agents=num_agents, overlap=overlap, task_description=task_description
        )
        # For each partition, optionally limit the number of tools
        if limit:
            partitions = [
                part[:limit] if len(part) > limit else part for part in partitions
            ]
        return partitions
