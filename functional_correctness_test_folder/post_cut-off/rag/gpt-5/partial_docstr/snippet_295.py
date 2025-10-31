from typing import Any, Dict, List, Optional, Tuple
import re
from collections import defaultdict


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
        self._tools: List[Dict[str, Any]] = list(tools or [])
        self._name_index: Dict[str, Dict[str, Any]] = {}
        self._search_blobs: Dict[int, str] = {}
        self._name_tokens: Dict[int, List[str]] = {}
        self._tags_tokens: Dict[int, List[str]] = {}
        self._desc_tokens: Dict[int, List[str]] = {}
        self._roles_tokens: Dict[int, List[str]] = {}
        self._stopwords = {
            'a', 'an', 'the', 'to', 'for', 'and', 'or', 'of', 'in', 'on', 'with', 'by', 'from', 'at', 'as',
            'is', 'are', 'be', 'can', 'using', 'use', 'do', 'make', 'run', 'build', 'this', 'that', 'it',
            'into', 'over', 'under', 'via', 'per', 'through', 'each', 'all', 'any', 'tool', 'tools', 'agent'
        }
        for idx, tool in enumerate(self._tools):
            name = str(tool.get('name', '') or '').strip()
            lname = name.lower()
            if lname and lname not in self._name_index:
                self._name_index[lname] = tool
            tags = tool.get('tags', [])
            if isinstance(tags, str):
                tags_list = [tags]
            elif isinstance(tags, list):
                tags_list = [str(t) for t in tags]
            else:
                tags_list = []
            roles = tool.get('roles', tool.get('role', []))
            if isinstance(roles, str):
                roles_list = [roles]
            elif isinstance(roles, list):
                roles_list = [str(r) for r in roles]
            else:
                roles_list = []
            category = str(tool.get('category', '') or '')
            description = str(tool.get('description', '') or '')
            blob_parts = [
                name,
                description,
                ' '.join(tags_list),
                ' '.join(roles_list),
                category
            ]
            blob = ' '.join([p for p in blob_parts if p]).lower()
            self._search_blobs[idx] = blob
            self._name_tokens[idx] = self._tokenize(name)
            self._tags_tokens[idx] = self._tokenize(' '.join(tags_list))
            self._desc_tokens[idx] = self._tokenize(description)
            self._roles_tokens[idx] = self._tokenize(' '.join(roles_list))

    def _tokenize(self, text: str) -> List[str]:
        toks = re.findall(r'[A-Za-z0-9_]+', (text or '').lower())
        return [t for t in toks if t and t not in self._stopwords]

    def _score_tool(self, tool_idx: int, keywords: List[str]) -> Tuple[float, int]:
        name_tokens = set(self._name_tokens.get(tool_idx, []))
        tags_tokens = set(self._tags_tokens.get(tool_idx, []))
        desc_tokens = set(self._desc_tokens.get(tool_idx, []))
        roles_tokens = set(self._roles_tokens.get(tool_idx, []))
        name_text = ' '.join(self._name_tokens.get(tool_idx, []))
        tags_text = ' '.join(self._tags_tokens.get(tool_idx, []))
        desc_text = ' '.join(self._desc_tokens.get(tool_idx, []))
        roles_text = ' '.join(self._roles_tokens.get(tool_idx, []))
        score = 0.0
        matched = 0
        for kw in keywords:
            if not kw:
                continue
            hit = False
            if kw in name_tokens:
                score += 5.0
                hit = True
            elif kw in name_text:
                score += 3.0
                hit = True
            if kw in tags_tokens:
                score += 3.0
                hit = True
            elif kw in tags_text:
                score += 1.5
                hit = True
            if kw in roles_tokens:
                score += 1.2
                hit = True
            elif kw in roles_text:
                score += 0.6
                hit = True
            if kw in desc_tokens:
                score += 1.0
                hit = True
            elif kw in desc_text:
                score += 0.5
                hit = True
            if hit:
                matched += 1
        tool = self._tools[tool_idx]
        priority = 0.0
        try:
            pr = tool.get('priority', 0)
            if isinstance(pr, (int, float)):
                priority = float(pr)
        except Exception:
            priority = 0.0
        score += matched * 0.1
        score += priority * 0.01
        return score, matched

    def _rank_tools(self, task_description: Optional[str]) -> List[int]:
        if not self._tools:
            return []
        if task_description and task_description.strip():
            kws = [k for k in self._tokenize(task_description)]
        else:
            kws = []
        if not kws:
            indexed = list(range(len(self._tools)))

            def key_fn(idx: int) -> Tuple[float, str]:
                tool = self._tools[idx]
                pr = tool.get('priority', 0)
                try:
                    prf = float(pr) if isinstance(pr, (int, float)) else 0.0
                except Exception:
                    prf = 0.0
                name = str(tool.get('name', '') or '').lower()
                return (-prf, name)
            return sorted(indexed, key=key_fn)
        scored: List[Tuple[int, float, int]] = []
        for idx in range(len(self._tools)):
            s, m = self._score_tool(idx, kws)
            scored.append((idx, s, m))
        scored.sort(
            key=lambda x: (-x[1], -x[2], str(self._tools[x[0]].get('name', '') or '').lower()))
        return [idx for idx, _, _ in scored]

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        '''
        Internal single-agent tool selection logic.
        '''
        if limit <= 0:
            return []
        ranked = self._rank_tools(task_description)
        top = ranked[:min(limit, len(ranked))]
        return [self._tools[i] for i in top]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        '''
        Internal multi-agent tool partitioning logic.
        '''
        if num_agents <= 1:
            return [self._select_for_task(task_description or '', limit=len(self._tools))]
        ranked = self._rank_tools(task_description)
        if not ranked:
            return [[] for _ in range(num_agents)]
        if overlap:
            full = [self._tools[i] for i in ranked]
            return [list(full) for _ in range(num_agents)]
        buckets: List[List[Dict[str, Any]]] = [[] for _ in range(num_agents)]
        for pos, idx in enumerate(ranked):
            buckets[pos % num_agents].append(self._tools[idx])
        return buckets

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        '''Select tools by their names (case-insensitive).'''
        if not tool_names:
            return []
        result: List[Dict[str, Any]] = []
        seen = set()
        for name in tool_names:
            if not name:
                continue
            lname = str(name).lower().strip()
            tool = self._name_index.get(lname)
            if tool is not None:
                if id(tool) not in seen:
                    result.append(tool)
                    seen.add(id(tool))
                continue
            candidates = [t for t in self._tools if lname in str(
                t.get('name', '') or '').lower()]
            for t in candidates:
                if id(t) not in seen:
                    result.append(t)
                    seen.add(id(t))
        return result

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        '''Filter tools for each role based on name patterns.'''
        out: Dict[str, List[Any]] = {}
        for role, patterns in (role_patterns or {}).items():
            rpats = [str(p).lower() for p in (patterns or [])]
            bucket: List[Dict[str, Any]] = []
            for tool in self._tools:
                name_l = str(tool.get('name', '') or '').lower()
                roles = tool.get('roles', tool.get('role', []))
                if isinstance(roles, str):
                    roles_list = [roles.lower()]
                elif isinstance(roles, list):
                    roles_list = [str(r).lower() for r in roles]
                else:
                    roles_list = []
                match_role_flag = role.lower() in roles_list
                match_name_flag = False
                if rpats:
                    for p in rpats:
                        if p == '*' or p in name_l:
                            match_name_flag = True
                            break
                if match_role_flag or (rpats and match_name_flag):
                    bucket.append(tool)
            out[role] = bucket
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
        if not keywords:
            return []
        kws = [k for k in self._tokenize(' '.join(keywords))]
        if not kws:
            return []
        matched: List[Dict[str, Any]] = []
        for idx in range(len(self._tools)):
            blob = self._search_blobs.get(idx, '')
            if match_all:
                ok = all(kw in blob for kw in kws)
            else:
                ok = any(kw in blob for kw in kws)
            if ok:
                matched.append(self._tools[idx])
        return matched

    def select_tools(self, task_description: str, num_agents: Optional[int] = None, overlap: bool = False, limit: int = 5) -> Any:
        '''
        Unified public interface for tool selection.
        - Single-agent (num_agents None or <=1): returns a flat list of top tools.
        - Multi-agent (num_agents >1): returns a list of tool lists, one per agent.
        Override this method to implement any custom logic.
        '''
        if num_agents is None or num_agents <= 1:
            return self._select_for_task(task_description or '', limit=max(0, int(limit)))
        partitions = self._partition_tools_for_multi_agent(
            int(num_agents), overlap=overlap, task_description=task_description or '')
        if limit is not None and limit >= 0:
            trimmed = [bucket[:limit] if limit > 0 else []
                       for bucket in partitions]
            return trimmed
        return partitions
