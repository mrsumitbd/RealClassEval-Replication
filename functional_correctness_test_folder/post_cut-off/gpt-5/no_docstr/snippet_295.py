from typing import List, Dict, Any, Optional, Tuple
import re
import math


class ToolSelector:
    def __init__(self, tools: List[Dict[str, Any]]):
        self._raw_tools: List[Dict[str, Any]] = tools or []
        self._norm_tools: List[Dict[str, Any]] = [
            self._normalize_tool(t) for t in self._raw_tools]

    def _normalize_tool(self, tool: Dict[str, Any]) -> Dict[str, Any]:
        name = str(tool.get("name") or tool.get("tool_name") or "").strip()
        desc = str(tool.get("description") or tool.get(
            "desc") or tool.get("doc") or "").strip()
        role = tool.get("role")
        role = str(role).strip() if role is not None else None
        # Determine the underlying callable/object
        obj = None
        for key in ("tool", "callable", "object", "fn", "func"):
            if key in tool:
                obj = tool[key]
                break
        # Fallback: if no object reference, return the original dict as object
        if obj is None:
            obj = tool
        return {
            "name": name,
            "description": desc,
            "role": role,
            "obj": obj,
            "raw": tool,
        }

    def _text_tokens(self, text: str) -> List[str]:
        return re.findall(r"[a-z0-9]+", text.lower())

    def _select_for_task(self, task_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        if not self._norm_tools:
            return []
        text = task_description or ""
        tokens = self._text_tokens(text)
        if not tokens:
            return self._norm_tools[: max(0, limit)]
        token_set = set(tokens)

        def score_tool(t: Dict[str, Any]) -> Tuple[float, int]:
            fields = " ".join(
                s for s in [t.get("name") or "", t.get("description") or "", t.get("role") or ""] if s
            ).lower()
            ftokens = set(self._text_tokens(fields))
            overlap = token_set & ftokens
            score = len(overlap)
            # Boost for name and role direct substring matches
            name = (t.get("name") or "").lower()
            role = (t.get("role") or "").lower()
            for tok in token_set:
                if tok and tok in name:
                    score += 1.5
                if role and tok in role:
                    score += 0.75
            # slight boost for longer descriptions containing more keywords
            score += min(1.0, len(overlap) * 0.1)
            # Negative tiny penalty for empty descriptions
            if not t.get("description"):
                score -= 0.05
            return (score, len(overlap))

        ranked = sorted(self._norm_tools,
                        key=lambda t: score_tool(t), reverse=True)
        if limit is None or limit <= 0:
            return ranked
        return ranked[:limit]

    def _partition_tools_for_multi_agent(
        self, num_agents: int, overlap: bool = False, task_description: Optional[str] = None
    ) -> List[List[Dict[str, Any]]]:
        num_agents = max(1, int(num_agents or 1))
        base_list = self._norm_tools if not task_description else self._select_for_task(
            task_description, limit=len(self._norm_tools))
        if overlap:
            return [list(base_list) for _ in range(num_agents)]
        n = len(base_list)
        if n == 0:
            return [[] for _ in range(num_agents)]
        # Round-robin partition to keep distribution fair and diverse
        partitions: List[List[Dict[str, Any]]] = [[]
                                                  for _ in range(num_agents)]
        for idx, tool in enumerate(base_list):
            partitions[idx % num_agents].append(tool)
        return partitions

    def _lookup_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        name_l = (name or "").strip().lower()
        for t in self._norm_tools:
            if t["name"].lower() == name_l:
                return t
        # fallback: substring match
        for t in self._norm_tools:
            if name_l and name_l in t["name"].lower():
                return t
        return None

    def select_by_names(self, tool_names: List[str]) -> List[Any]:
        if not tool_names:
            return []
        result: List[Any] = []
        seen = set()
        for nm in tool_names:
            t = self._lookup_by_name(nm)
            if t and id(t["obj"]) not in seen:
                seen.add(id(t["obj"]))
                result.append(t["obj"])
        return result

    def _pattern_match(self, text: str, pattern: str) -> bool:
        if not pattern:
            return False
        text_l = text.lower()
        pat = pattern.strip()
        # Regex if enclosed in /.../ or prefixed with re:
        if (pat.startswith("/") and pat.endswith("/") and len(pat) >= 2) or pat.lower().startswith("re:"):
            expr = pat[1:-1] if pat.startswith("/") else pat[3:]
            try:
                return re.search(expr, text, flags=re.IGNORECASE) is not None
            except re.error:
                return pat.lower() in text_l
        # Default: case-insensitive substring
        return pat.lower() in text_l

    def filter_by_roles(self, role_patterns: Dict[str, List[str]]) -> Dict[str, List[Any]]:
        result: Dict[str, List[Any]] = {}
        if not role_patterns:
            return result
        for label, patterns in role_patterns.items():
            collected: List[Any] = []
            pats = patterns or []
            for t in self._norm_tools:
                role = t.get("role") or ""
                if any(self._pattern_match(role, p) for p in pats):
                    collected.append(t["obj"])
            result[label] = collected
        return result

    def filter_by_keywords(self, keywords: List[str], match_all: bool = False) -> List[Any]:
        if not keywords:
            return [t["obj"] for t in self._norm_tools]
        kw = [k.strip().lower() for k in keywords if k and k.strip()]
        if not kw:
            return [t["obj"] for t in self._norm_tools]
        result: List[Any] = []
        for t in self._norm_tools:
            blob = " ".join(
                s for s in [t.get("name") or "", t.get("description") or "", t.get("role") or ""] if s
            ).lower()
            hits = [k in blob for k in kw]
            if (match_all and all(hits)) or (not match_all and any(hits)):
                result.append(t["obj"])
        return result

    def select_tools(
        self, task_description: str, num_agents: Optional[int] = None, overlap: bool = False, limit: int = 5
    ) -> Any:
        if not num_agents or num_agents <= 1:
            selected = self._select_for_task(task_description, limit=limit)
            return [t["obj"] for t in selected]
        # Multi-agent selection: select a focused pool then partition
        pool = self._select_for_task(
            task_description, limit=max(limit, num_agents))
        if overlap:
            return [[t["obj"] for t in pool] for _ in range(max(1, int(num_agents)))]
        # Partition pool among agents
        partitions: List[List[Dict[str, Any]]] = [[]
                                                  for _ in range(num_agents)]
        for idx, tool in enumerate(pool):
            partitions[idx % num_agents].append(tool)
        return [[t["obj"] for t in part] for part in partitions]
