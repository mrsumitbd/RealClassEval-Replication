from typing import Any, Dict, List, Optional
import re
import fnmatch
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
            name = str(t.get('name', '')).strip()
            lname = name.lower()
            if lname:
                self._name_index[lname] = t
            for alias in t.get('aliases', []) or []:
                if isinstance(alias, str) and alias.strip():
                    self._name_index[alias.strip().lower()] = t

    def _normalize(self, s: Any) -> str:
        return str(s or '').strip().lower()

    def _tokenize(self, text: str) -> List[str]:
        t = self._normalize(text)
        return [tok for tok in re.findall(r'\w+', t) if len(tok) > 1]

    def _tool_tags(self, tool: Dict[str, Any]) -> List[str]:
        tags: List[str] = []
        for key in ('tags', 'keywords', 'labels', 'categories'):
            val = tool.get(key)
            if isinstance(val, list):
                for v in val:
                    if isinstance(v, str):
                        tags.append(self._normalize(v))
        if isinstance(tool.get('category'), str):
            tags.append(self._normalize(tool['category']))
        return tags

    def _score_tool(self, tokens: List[str], tool: Dict[str, Any]) -> float:
        if not tokens:
            # Base score from optional metadata for deterministic ordering
            base = 0.0
            base += float(tool.get('priority', 0) or 0)
            base += float(tool.get('popularity', 0) or 0) * 0.01
            base += float(tool.get('usage_count', 0) or 0) * 0.001
            return base

        name = self._normalize(tool.get('name', ''))
        desc = self._normalize(tool.get('description', ''))
        tags = self._tool_tags(tool)

        score = 0.0
        for tok in tokens:
            if not tok:
                continue
            # Name match (substring)
            if tok in name:
                score += 3.0
            # Description match (substring)
            if tok in desc:
                score += 1.0
            # Exact tag match
            if tok in tags:
                score += 2.0
            # Roles or functions metadata (if present)
            roles = tool.get('roles') or []
            if isinstance(roles, list) and any(self._normalize(r) == tok for r in roles if isinstance(r, str)):
                score += 1.5
            functions = tool.get('functions') or []
            if isinstance(functions, list):
                for f in functions:
                    if isinstance(f, dict):
                        fname = self._normalize(f.get('name', ''))
                        fdesc = self._normalize(f.get('description', ''))
                        if tok in fname:
                            score += 1.5
                        if tok in fdesc:
                            score += 0.5
                    elif isinstance(f, str):
                        if tok in self._normalize(f):
                            score += 1.0

        score += float(tool.get('priority', 0) or 0)
        score += float(tool.get('popularity', 0) or 0) * 0.01
        score += float(tool.get('usage_count', 0) or 0) * 0.001
        if tool.get('deprecated') or tool.get('disabled'):
            score -= 1000.0
        return score

    def _rank_tools(self, task_description: Optional[str]) -> List[Dict[str, Any]]:
        tokens = self._tokenize(task_description or '')
        ranked = sorted(
            self.tools,
            key=lambda t: (-self._score_tool(tokens, t),
                           self._normalize(t.get('name', '')))
        )
        # Filter out disabled heavily penalized tools if present
        return [t for t in ranked if not t.get('disabled')]

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        '''
        Internal single-agent tool selection logic.
        '''
        ranked = self._rank_tools(task_description)
        if limit is None or limit <= 0:
            return ranked
        return ranked[: min(limit, len(ranked))]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        '''
        Internal multi-agent tool partitioning logic.
        '''
        num_agents = max(1, int(num_agents))
        ranked = self._rank_tools(task_description)
        if not ranked:
            return [[] for _ in range(num_agents)]

        if overlap:
            return [ranked[:] for _ in range(num_agents)]

        buckets: List[List[Dict[str, Any]]] = [[] for _ in range(num_agents)]
        for i, tool in enumerate(ranked):
            buckets[i % num_agents].append(tool)
        return buckets

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        '''Select tools by their names (case-insensitive).'''
        result: List[Dict[str, Any]] = []
        seen: set = set()
        for name in tool_names or []:
            lname = self._normalize(name)
            t = self._name_index.get(lname)
            if t is None:
                # Fallback: partial match by name
                candidates = [tool for tool in self.tools if lname in self._normalize(
                    tool.get('name', ''))]
                if candidates:
                    t = candidates[0]
            if t and id(t) not in seen:
                seen.add(id(t))
                result.append(t)
        return result

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        '''Filter tools for each role based on name patterns.'''
        out: Dict[str, List[Dict[str, Any]]] = {}
        for role, patterns in (role_patterns or {}).items():
            role_l = self._normalize(role)
            pats = [self._normalize(p) for p in (patterns or [])]
            matched: List[Dict[str, Any]] = []
            for t in self.tools:
                name_l = self._normalize(t.get('name', ''))
                roles = t.get('roles') or []
                has_role = any(self._normalize(
                    r) == role_l for r in roles if isinstance(r, str))
                name_match = any(fnmatch.fnmatch(name_l, p) for p in pats if p)
                if has_role or name_match:
                    matched.append(t)
            out[role] = matched
        return out

    def filter_by_keywords(self, keywords: List[str], match_all: bool = False) -> List[Any]:
        '''
        Filter tools that match specified keywords in name or description.
        Args:
            keywords: List of keywords to match
            match_all: If True, tools must match all keywords. If False, match any keyword.
        Returns:
            List of tools matching the criteria
        '''
        toks = [self._normalize(k)
                for k in (keywords or []) if self._normalize(k)]
        if not toks:
            return self.tools[:]

        def tool_matches(t: Dict[str, Any]) -> bool:
            hay = ' '.join([
                self._normalize(t.get('name', '')),
                self._normalize(t.get('description', '')),
                ' '.join(self._tool_tags(t))
            ])
            if match_all:
                return all(tok in hay for tok in toks)
            return any(tok in hay for tok in toks)

        matched = [t for t in self.tools if tool_matches(t)]
        # Rank matched by relevance to the provided keywords
        ranked = sorted(
            matched,
            key=lambda t: (-self._score_tool(toks, t),
                           self._normalize(t.get('name', '')))
        )
        return ranked

    def select_tools(self, task_description: str, num_agents: Optional[int] = None, overlap: bool = False, limit: int = 5) -> Any:
        '''
        Unified public interface for tool selection.
        - Single-agent (num_agents None or <=1): returns a flat list of top tools.
        - Multi-agent (num_agents >1): returns a list of tool lists, one per agent.
        Override this method to implement any custom logic.
        '''
        if num_agents is None or num_agents <= 1:
            return self._select_for_task(task_description, limit=limit)

        num_agents = max(1, int(num_agents))
        # Start from a ranked list
        ranked = self._rank_tools(task_description)

        if overlap:
            per_agent = ranked[: min(limit, len(ranked))
                               ] if limit and limit > 0 else ranked[:]
            return [per_agent[:] for _ in range(num_agents)]

        # Disjoint allocation with round-robin for fairness
        buckets: List[List[Dict[str, Any]]] = [[] for _ in range(num_agents)]
        for i, tool in enumerate(ranked):
            buckets[i % num_agents].append(tool)

        if limit and limit > 0:
            buckets = [b[: min(limit, len(b))] for b in buckets]

            # If some buckets are short due to small tool pool, top up from remaining ranked tools
            total_needed = num_agents * limit
            if len(ranked) < total_needed:
                # Gather remainder not yet in buckets
                assigned_ids = {id(t) for b in buckets for t in b}
                remainder = [t for t in ranked if id(t) not in assigned_ids]
                # Top up in round-robin
                bi = 0
                for t in remainder:
                    if len(buckets[bi]) < limit:
                        buckets[bi].append(t)
                    bi = (bi + 1) % num_agents
                    if all(len(b) >= limit for b in buckets):
                        break

        return buckets
