from typing import Any, Dict, List, Optional, Tuple, Set
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
            name = str(t.get('name') or t.get('id') or '').strip()
            if name:
                self._name_index[name.lower()] = t
            aliases = t.get('aliases') or []
            if isinstance(aliases, (list, tuple)):
                for alias in aliases:
                    try:
                        self._name_index[str(alias).lower()] = t
                    except Exception:
                        continue

    @staticmethod
    def _tokenize(text: Optional[str]) -> Set[str]:
        if not text:
            return set()
        tokens = re.findall(r"[A-Za-z0-9]+", text.lower())
        stop = {
            'the', 'a', 'an', 'for', 'and', 'or', 'to', 'of', 'in', 'on', 'with', 'by', 'from',
            'this', 'that', 'these', 'those', 'is', 'are', 'be', 'as', 'it', 'at', 'into',
            'about', 'across', 'tool', 'tools', 'agent', 'agents', 'use', 'using', 'run'
        }
        return {t for t in tokens if t not in stop and len(t) > 1}

    @staticmethod
    def _ensure_list(val: Any) -> List[str]:
        if val is None:
            return []
        if isinstance(val, str):
            return [val]
        if isinstance(val, (list, tuple, set)):
            try:
                return [str(v) for v in val]
            except Exception:
                return [str(v) for v in list(val)]
        return [str(val)]

    def _score_tool(self, tool: Dict[str, Any], query_tokens: Set[str]) -> float:
        if not query_tokens:
            base_priority = float(tool.get('priority')
                                  or tool.get('popularity') or 0)
            return base_priority
        name = str(tool.get('name') or tool.get('id') or '').lower()
        desc = str(tool.get('description') or '').lower()
        tags = [s.lower() for s in self._ensure_list(tool.get('tags')
                                                     or tool.get('keywords') or tool.get('capabilities'))]
        roles = [s.lower() for s in self._ensure_list(tool.get('roles'))]

        name_tokens = self._tokenize(name)
        desc_tokens = self._tokenize(desc)
        tag_tokens: Set[str] = set()
        for t in tags:
            tag_tokens |= self._tokenize(t)
        role_tokens: Set[str] = set()
        for r in roles:
            role_tokens |= self._tokenize(r)

        # Weighted matches
        w_name = 3.0
        w_tags = 2.0
        w_desc = 1.0
        w_roles = 1.5

        score = 0.0
        score += w_name * len(query_tokens & name_tokens)
        score += w_tags * len(query_tokens & tag_tokens)
        score += w_desc * len(query_tokens & desc_tokens)
        score += w_roles * len(query_tokens & role_tokens)

        # Substring bonus for exact phrase presence in name/desc
        joined_query = " ".join(sorted(query_tokens))
        if joined_query and joined_query in name:
            score += 1.0
        if joined_query and joined_query in desc:
            score += 0.5

        # Numeric priority/popularity as small tie-breaker
        priority = 0.0
        try:
            priority = float(tool.get('priority')
                             or tool.get('popularity') or 0.0)
        except Exception:
            priority = 0.0
        score += 0.01 * max(0.0, priority)

        return score

    def _rank_tools(self, task_description: Optional[str]) -> List[Tuple[Dict[str, Any], float]]:
        q_tokens = self._tokenize(task_description or "")
        ranked: List[Tuple[Dict[str, Any], float]] = []
        for t in self.tools:
            ranked.append((t, self._score_tool(t, q_tokens)))
        ranked.sort(
            key=lambda x: (
                -x[1],
                -float(x[0].get('priority') or x[0].get('popularity') or 0.0),
                str(x[0].get('name') or x[0].get('id') or '').lower()
            )
        )
        return ranked

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        '''
        Internal single-agent tool selection logic.
        '''
        ranked = self._rank_tools(task_description)
        # Prefer tools with positive scores; if not enough, include next best
        positives = [t for t, s in ranked if s > 0]
        if len(positives) >= limit:
            return positives[:limit]
        # Fill remainder
        selected = positives[:]
        if len(selected) < limit:
            for t, _ in ranked:
                if t in selected:
                    continue
                selected.append(t)
                if len(selected) >= limit:
                    break
        return selected[:limit]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        '''
        Internal multi-agent tool partitioning logic.
        '''
        num_agents = max(1, int(num_agents))
        ranked_tools = [t for t, _ in self._rank_tools(task_description or "")]
        if not ranked_tools:
            return [[] for _ in range(num_agents)]

        if overlap:
            # Every agent gets the full ranked list
            return [ranked_tools[:] for _ in range(num_agents)]

        # Non-overlapping: round-robin distribution
        partitions: List[List[Dict[str, Any]]] = [[]
                                                  for _ in range(num_agents)]
        for idx, tool in enumerate(ranked_tools):
            partitions[idx % num_agents].append(tool)
        return partitions

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        '''Select tools by their names (case-insensitive).'''
        result: List[Dict[str, Any]] = []
        seen: Set[int] = set()
        for name in tool_names or []:
            key = str(name).lower()
            tool = self._name_index.get(key)
            if tool is not None:
                tool_id = id(tool)
                if tool_id not in seen:
                    result.append(tool)
                    seen.add(tool_id)
        return result

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        '''Filter tools for each role based on name patterns.'''
        out: Dict[str, List[Dict[str, Any]]] = {}
        for role, patterns in (role_patterns or {}).items():
            role_l = str(role).lower()
            pats = [p.lower() for p in (patterns or [])]
            matched: List[Dict[str, Any]] = []
            for t in self.tools:
                name_l = str(t.get('name') or t.get('id') or '').lower()
                tool_roles = [str(r).lower()
                              for r in self._ensure_list(t.get('roles'))]
                matches_role = role_l in tool_roles
                matches_name = any(fnmatch.fnmatch(name_l, p)
                                   for p in pats) if pats else False
                if (pats and (matches_name or matches_role)) or (not pats and matches_role):
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
        kws = [str(k).lower() for k in (keywords or []) if str(k).strip()]
        if not kws:
            return []
        results: List[Dict[str, Any]] = []
        for t in self.tools:
            hay = " ".join([
                str(t.get('name') or t.get('id') or ''),
                str(t.get('description') or ''),
                " ".join(self._ensure_list(t.get('tags') or t.get(
                    'keywords') or t.get('capabilities'))),
                " ".join(self._ensure_list(t.get('roles')))
            ]).lower()
            if match_all:
                ok = all(k in hay for k in kws)
            else:
                ok = any(k in hay for k in kws)
            if ok:
                results.append(t)
        return results

    def select_tools(self, task_description: str, num_agents: Optional[int] = None, overlap: bool = False, limit: int = 5) -> Any:
        '''
        Unified public interface for tool selection.
        - Single-agent (num_agents None or <=1): returns a flat list of top tools.
        - Multi-agent (num_agents >1): returns a list of tool lists, one per agent.
        Override this method to implement any custom logic.
        '''
        if num_agents is None or int(num_agents) <= 1:
            return self._select_for_task(task_description, limit=limit)

        n_agents = max(2, int(num_agents))
        if overlap:
            top_k = self._select_for_task(task_description, limit=limit)
            return [top_k[:] for _ in range(n_agents)]

        # Non-overlapping: distribute the top (limit * n_agents) tools round-robin
        ranked = [t for t, _ in self._rank_tools(task_description)]
        top = ranked[: max(0, min(len(ranked), limit * n_agents))]
        partitions: List[List[Dict[str, Any]]] = [[] for _ in range(n_agents)]
        for i in range(len(top)):
            bucket = i % n_agents
            if len(partitions[bucket]) < limit:
                partitions[bucket].append(top[i])
            else:
                # Find next bucket with capacity
                placed = False
                for j in range(n_agents):
                    b = (bucket + j) % n_agents
                    if len(partitions[b]) < limit:
                        partitions[b].append(top[i])
                        placed = True
                        break
                if not placed:
                    break
        return partitions
