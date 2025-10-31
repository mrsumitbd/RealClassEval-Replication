from typing import List, Dict, Any, Optional, Any as AnyType
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
        self.tools: List[Dict[str, Any]] = list(tools or [])
        self._name_index: Dict[str, Dict[str, Any]] = {}
        for t in self.tools:
            name = str(t.get("name", "")).strip()
            if name:
                self._name_index[name.lower()] = t

    def _textify(self, tool: Dict[str, Any]) -> str:
        parts = []
        name = tool.get("name")
        desc = tool.get("description") or tool.get("desc")
        kws = tool.get("keywords") or tool.get("tags")
        alias = tool.get("aliases") or tool.get("alias")
        roles = tool.get("roles")
        if name:
            parts.append(str(name))
        if desc:
            parts.append(str(desc))
        if kws and isinstance(kws, (list, tuple, set)):
            parts.extend([str(x) for x in kws])
        if alias and isinstance(alias, (list, tuple, set)):
            parts.extend([str(x) for x in alias])
        if roles and isinstance(roles, (list, tuple, set)):
            parts.extend([str(x) for x in roles])
        return " ".join(parts)

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def _score_tool(self, tool: Dict[str, Any], task_description: str) -> float:
        if not task_description:
            return 0.0
        task_text = task_description.lower()
        task_tokens = set(self._tokenize(task_text))
        tool_text = self._textify(tool).lower()
        tool_tokens = set(self._tokenize(tool_text))

        token_overlap = len(task_tokens & tool_tokens)

        substr_bonus = 0
        # Simple substring hints from name/description
        name = str(tool.get("name", "")).lower()
        desc = str(tool.get("description", tool.get("desc", ""))).lower()
        for token in task_tokens:
            if len(token) >= 4:
                if token in name:
                    substr_bonus += 2
                elif token in desc:
                    substr_bonus += 1

        # Prefer tools explicitly marked with keywords that appear
        kws = tool.get("keywords") or tool.get("tags") or []
        if isinstance(kws, (list, tuple, set)):
            kws_lower = {str(k).lower() for k in kws}
            keyword_overlap = len(kws_lower & task_tokens)
        else:
            keyword_overlap = 0

        # Light weighting
        score = token_overlap * 2 + substr_bonus + keyword_overlap * 3

        # Small bias for tools with roles matching task words like "planner", "coder", etc.
        roles = tool.get("roles") or []
        if isinstance(roles, (list, tuple, set)):
            roles_lower = {str(r).lower() for r in roles}
            score += len(roles_lower & task_tokens)

        return float(score)

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        '''
        Internal single-agent tool selection logic.
        '''
        if not self.tools:
            return []
        scored = [(self._score_tool(t, task_description), idx, t)
                  for idx, t in enumerate(self.tools)]
        scored.sort(key=lambda x: (-x[0], x[1]))
        top = [t for s, _, t in scored if s > 0]
        if not top:
            # If no positive scores, fall back to first tools
            top = [t for _, _, t in scored]
        return top[: max(0, int(limit))]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        '''
        Internal multi-agent tool partitioning logic.
        '''
        num_agents = int(num_agents) if num_agents else 0
        if num_agents <= 0:
            return []
        if not self.tools:
            return [[] for _ in range(num_agents)]

        # Rank tools by task_description if provided
        if task_description:
            ranked = self._select_for_task(
                task_description, limit=len(self.tools))
        else:
            ranked = list(self.tools)

        n = len(ranked)
        if num_agents == 1:
            return [ranked]

        # Split into nearly equal contiguous chunks preserving order
        base = n // num_agents
        rem = n % num_agents
        chunks = []
        start = 0
        for i in range(num_agents):
            size = base + (1 if i < rem else 0)
            end = start + size
            chunks.append(ranked[start:end])
            start = end

        if not overlap:
            return chunks

        # Add overlap by including neighbor boundary items without duplicates
        overlapped = []
        for i, chunk in enumerate(chunks):
            extended = list(chunk)
            if i > 0 and chunks[i - 1]:
                prev_tail = chunks[i - 1][-1]
                if prev_tail not in extended:
                    extended.insert(0, prev_tail)
            if i < len(chunks) - 1 and chunks[i + 1]:
                next_head = chunks[i + 1][0]
                if next_head not in extended:
                    extended.append(next_head)
            overlapped.append(extended)
        return overlapped

    def select_by_names(self, tool_names: List[str]) -> List[AnyType]:
        '''Select tools by their names (case-insensitive).'''
        if not tool_names:
            return []
        result = []
        wanted = {str(n).strip().lower() for n in tool_names if str(n).strip()}
        if not wanted:
            return []

        # Build alias map
        alias_map: Dict[str, Dict[str, Any]] = {}
        for t in self.tools:
            name = str(t.get("name", "")).strip().lower()
            if name:
                alias_map[name] = t
            aliases = t.get("aliases") or t.get("alias") or []
            if isinstance(aliases, (list, tuple, set)):
                for a in aliases:
                    a_norm = str(a).strip().lower()
                    if a_norm:
                        alias_map[a_norm] = t

        seen = set()
        for w in wanted:
            t = alias_map.get(w)
            if t and id(t) not in seen:
                result.append(t)
                seen.add(id(t))
        return result

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[AnyType]]:
        '''Filter tools for each role based on name patterns.'''
        out: Dict[str, List[AnyType]] = {}
        if not role_patterns:
            return out

        for role, patterns in role_patterns.items():
            if not patterns:
                out[role] = []
                continue
            pats = [str(p).lower() for p in patterns if str(p).strip()]
            matched = []
            seen = set()
            for t in self.tools:
                hay_name = str(t.get("name", "")).lower()
                hay_desc = str(t.get("description", t.get("desc", ""))).lower()
                text = hay_name + " " + hay_desc
                if any(p in text for p in pats):
                    if id(t) not in seen:
                        matched.append(t)
                        seen.add(id(t))
            out[role] = matched
        return out

    def filter_by_keywords(self, keywords: List[str], match_all: bool = False) -> List[AnyType]:
        '''
        Filter tools that match specified keywords in name or description.
        Args:
            keywords: List of keywords to match
            match_all: If True, tools must match all keywords. If False, match any keyword.
        Returns:
            List of tools matching the criteria
        '''
        if not keywords:
            return []
        kws = [str(k).lower() for k in keywords if str(k).strip()]
        if not kws:
            return []

        matched = []
        for t in self.tools:
            text = self._textify(t).lower()
            if match_all:
                if all(k in text for k in kws):
                    matched.append(t)
            else:
                if any(k in text for k in kws):
                    matched.append(t)
        return matched

    def select_tools(self, task_description: str, num_agents: Optional[int] = None, overlap: bool = False, limit: int = 5) -> Any:
        '''
        Unified public interface for tool selection.
        - Single-agent (num_agents None or <=1): returns a flat list of top tools.
        - Multi-agent (num_agents >1): returns a list of tool lists, one per agent.
        Override this method to implement any custom logic.
        '''
        if not num_agents or num_agents <= 1:
            return self._select_for_task(task_description, limit=limit)

        partitions = self._partition_tools_for_multi_agent(
            int(num_agents), overlap=overlap, task_description=task_description)
        if limit is not None:
            lim = max(0, int(limit))
            partitions = [p[:lim] for p in partitions]
        return partitions
