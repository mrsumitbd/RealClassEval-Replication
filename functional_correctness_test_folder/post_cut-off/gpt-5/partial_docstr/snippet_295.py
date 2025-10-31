from typing import Any, Dict, List, Optional, Iterable, Sequence, Tuple
import re
from fnmatch import fnmatchcase


class ToolSelector:

    def __init__(self, tools: List[Dict[str, Any]]):
        '''
        Initialize with available tools.
        Args:
            tools: List of tool definitions from ToolManager
        '''
        self._tools: List[Any] = list(tools) if tools is not None else []
        self._name_to_tool: Dict[str, Any] = {}
        for t in self._tools:
            nm = self._get_name(t)
            if nm:
                self._name_to_tool[nm.lower()] = t
        # cache of rankings by task text
        self._rank_cache: Dict[str, List[Any]] = {}

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        ranked = self._rank_tools(task_description or "")
        if limit is None or limit <= 0:
            return ranked[:]
        return ranked[: min(limit, len(ranked))]

    def _partition_tools_for_multi_agent(self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None) -> List[List[Dict[str, Any]]]:
        if num_agents is None or num_agents <= 0:
            return []
        if overlap:
            # Give each agent the same top set (default limit of 5)
            selected = self._select_for_task(task_description or "", limit=5)
            return [selected[:] for _ in range(num_agents)]
        # No overlap: partition a ranked subset (or all tools if no task)
        if task_description:
            ranked = self._rank_tools(task_description)
        else:
            ranked = self._tools[:]
        top_k = len(ranked)
        if top_k == 0:
            return [[] for _ in range(num_agents)]
        # Evenly distribute while preserving order
        base = top_k // num_agents
        rem = top_k % num_agents
        result: List[List[Any]] = []
        start = 0
        for i in range(num_agents):
            size = base + (1 if i < rem else 0)
            end = start + size
            result.append(ranked[start:end])
            start = end
        return result

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        '''Select tools by their names (case-insensitive).'''
        if not tool_names:
            return []
        out: List[Any] = []
        seen = set()
        for nm in tool_names:
            if not isinstance(nm, str):
                continue
            key = nm.strip().lower()
            if not key:
                continue
            tool = self._name_to_tool.get(key)
            if tool is not None and id(tool) not in seen:
                out.append(tool)
                seen.add(id(tool))
        return out

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        result: Dict[str, List[Any]] = {}
        if not role_patterns:
            return result
        for role_label, patterns in role_patterns.items():
            if not patterns:
                result[role_label] = []
                continue
            lower_patterns = [p.lower()
                              for p in patterns if isinstance(p, str)]
            matched: List[Any] = []
            for tool in self._tools:
                roles = self._get_roles(tool)
                if not roles:
                    continue
                lr = [r.lower() for r in roles if isinstance(r, str)]
                if any(any(fnmatchcase(r, pat) for pat in lower_patterns) for r in lr):
                    matched.append(tool)
            result[role_label] = matched
        return result

    def filter_by_keywords(self, keywords: List[str], match_all: bool = False) -> List[Any]:
        if not keywords:
            return []
        kw = [k.strip().lower()
              for k in keywords if isinstance(k, str) and k.strip()]
        if not kw:
            return []
        out: List[Any] = []
        for tool in self._tools:
            tokens = self._tool_tokens(tool)
            if match_all:
                if all(k in tokens for k in kw):
                    out.append(tool)
            else:
                if any(k in tokens for k in kw):
                    out.append(tool)
        return out

    def select_tools(self, task_description: str, num_agents: Optional[int] = None, overlap: bool = False, limit: int = 5) -> Any:
        '''
        Unified public interface for tool selection.
        - Single-agent (num_agents None or <=1): returns a flat list of top tools.
        - Multi-agent (num_agents >1): returns a list of tool lists, one per agent.
        Override this method to implement any custom logic.
        '''
        if num_agents is None or num_agents <= 1:
            return self._select_for_task(task_description or "", limit=limit)
        # multi-agent
        if overlap:
            selected = self._select_for_task(
                task_description or "", limit=max(1, limit))
            return [selected[:] for _ in range(num_agents)]
        # No overlap: take top limit*num_agents and partition evenly
        ranked = self._rank_tools(task_description or "")
        if limit is None or limit <= 0:
            top_k = len(ranked)
        else:
            top_k = min(len(ranked), max(1, limit) * num_agents)
        subset = ranked[:top_k]
        # Even partition
        base = top_k // num_agents
        rem = top_k % num_agents
        parts: List[List[Any]] = []
        start = 0
        for i in range(num_agents):
            size = base + (1 if i < rem else 0)
            end = start + size
            parts.append(subset[start:end])
            start = end
        return parts

    # ----------------- Helpers -----------------

    def _get_name(self, tool: Any) -> Optional[str]:
        if tool is None:
            return None
        if isinstance(tool, dict):
            for key in ("name", "tool_name", "id", "identifier", "title"):
                if key in tool and isinstance(tool[key], str):
                    return tool[key]
            return None
        # object with attribute
        for attr in ("name", "tool_name", "id", "identifier", "title"):
            val = getattr(tool, attr, None)
            if isinstance(val, str):
                return val
        return None

    def _get_description(self, tool: Any) -> str:
        if tool is None:
            return ""
        if isinstance(tool, dict):
            for key in ("description", "doc", "docs", "summary", "help"):
                v = tool.get(key)
                if isinstance(v, str):
                    return v
        else:
            for attr in ("description", "doc", "docs", "summary", "help", "__doc__"):
                v = getattr(tool, attr, None)
                if isinstance(v, str):
                    return v
        return ""

    def _get_keywords(self, tool: Any) -> List[str]:
        vals: List[str] = []
        if tool is None:
            return vals
        if isinstance(tool, dict):
            for key in ("keywords", "tags", "labels"):
                v = tool.get(key)
                if isinstance(v, (list, tuple, set)):
                    vals.extend([str(x) for x in v])
        else:
            for attr in ("keywords", "tags", "labels"):
                v = getattr(tool, attr, None)
                if isinstance(v, (list, tuple, set)):
                    vals.extend([str(x) for x in v])
        return vals

    def _get_roles(self, tool: Any) -> List[str]:
        vals: List[str] = []
        if tool is None:
            return vals
        if isinstance(tool, dict):
            v = tool.get("roles") if "roles" in tool else tool.get("role")
            if isinstance(v, (list, tuple, set)):
                vals.extend([str(x) for x in v])
            elif isinstance(v, str):
                vals.append(v)
        else:
            v = getattr(tool, "roles", None)
            if v is None:
                v = getattr(tool, "role", None)
            if isinstance(v, (list, tuple, set)):
                vals.extend([str(x) for x in v])
            elif isinstance(v, str):
                vals.append(v)
        return vals

    _split_re = re.compile(r"[^\w]+")

    def _tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        return [t for t in self._split_re.split(text.lower()) if t]

    def _tool_tokens(self, tool: Any) -> List[str]:
        tokens: List[str] = []
        name = self._get_name(tool)
        desc = self._get_description(tool)
        keys = self._get_keywords(tool)
        roles = self._get_roles(tool)
        if name:
            tokens.extend(self._tokenize(name))
        if desc:
            tokens.extend(self._tokenize(desc))
        for k in keys:
            tokens.extend(self._tokenize(k))
        for r in roles:
            tokens.extend(self._tokenize(r))
        return tokens

    def _rank_tools(self, task_description: str) -> List[Any]:
        text = (task_description or "").strip().lower()
        if text in self._rank_cache:
            return self._rank_cache[text][:]
        query_tokens = self._tokenize(text)
        qset = set(query_tokens)
        if not self._tools:
            self._rank_cache[text] = []
            return []
        scored: List[Tuple[float, int, Any]] = []
        for idx, tool in enumerate(self._tools):
            name = self._get_name(tool) or ""
            desc = self._get_description(tool)
            keys = self._get_keywords(tool)
            roles = self._get_roles(tool)

            name_tokens = set(self._tokenize(name))
            desc_tokens = set(self._tokenize(desc))
            key_tokens = set()
            for k in keys:
                key_tokens.update(self._tokenize(k))
            role_tokens = set()
            for r in roles:
                role_tokens.update(self._tokenize(r))

            # Weighted overlap scoring
            s = 0.0
            if qset:
                s += 3.0 * len(qset & name_tokens)
                s += 2.0 * len(qset & key_tokens)
                s += 2.0 * len(qset & role_tokens)
                s += 1.0 * len(qset & desc_tokens)
            # Substring bonus for exact keyword presence in name/desc
            if text and name and text in name.lower():
                s += 0.5
            if text and desc and text in desc.lower():
                s += 0.25
            # Fallback mild heuristic: prefer tools with more metadata
            meta_bonus = 0.0
            if name:
                meta_bonus += 0.05
            if desc:
                meta_bonus += 0.05
            if keys:
                meta_bonus += min(0.2, 0.02 * len(keys))
            if roles:
                meta_bonus += min(0.2, 0.02 * len(roles))
            s += meta_bonus
            scored.append((-(s), idx, tool))  # negative for ascending sort

        scored.sort()
        ranked = [t for _, _, t in scored]
        self._rank_cache[text] = ranked[:]
        return ranked[:]
