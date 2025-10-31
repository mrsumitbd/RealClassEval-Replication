from typing import Optional, Dict, Any, Iterable


class CacheKeyBuilder:
    '''Helper class to build standardized cache keys.'''

    @staticmethod
    def _normalize_str(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        s = str(value).strip()
        return s if s else None

    @staticmethod
    def _normalize_int(value: Optional[int]) -> Optional[int]:
        if value is None:
            return None
        return int(value)

    @staticmethod
    def _normalize_bool(value: bool) -> int:
        return 1 if bool(value) else 0

    @staticmethod
    def _normalize_list(values: Optional[Iterable[str]]) -> Optional[list]:
        if values is None:
            return None
        norm = []
        for v in values:
            if v is None:
                continue
            s = str(v).strip().lower()
            if s:
                norm.append(s)
        if not norm:
            return None
        # Deduplicate and sort for determinism
        return sorted(set(norm))

    @staticmethod
    def _build_key(namespace: str, parts: Dict[str, Any]) -> str:
        segments = [namespace]
        for k in sorted(parts.keys()):
            v = parts[k]
            if isinstance(v, list):
                seg = ",".join(v)
            elif v is None:
                seg = "*"
            else:
                seg = str(v)
            segments.append(f"{k}:{seg}")
        return "|".join(segments)

    @staticmethod
    def alerts_key(agent_id: Optional[str] = None, time_range: str = '24h', level: Optional[int] = None) -> Dict[str, Any]:
        agent = CacheKeyBuilder._normalize_str(agent_id)
        tr = CacheKeyBuilder._normalize_str(time_range) or '24h'
        lvl = CacheKeyBuilder._normalize_int(level)
        parts = {
            'agent': agent or '*',
            'time': tr,
            'level': lvl
        }
        return {
            'namespace': 'alerts',
            'parts': parts,
            'key': CacheKeyBuilder._build_key('alerts', parts)
        }

    @staticmethod
    def agent_health_key(agent_id: str) -> Dict[str, Any]:
        agent = CacheKeyBuilder._normalize_str(agent_id)
        parts = {
            'agent': agent or '*'
        }
        return {
            'namespace': 'agent_health',
            'parts': parts,
            'key': CacheKeyBuilder._build_key('agent_health', parts)
        }

    @staticmethod
    def vulnerabilities_key(agent_id: Optional[str] = None, severity: Optional[str] = None) -> Dict[str, Any]:
        agent = CacheKeyBuilder._normalize_str(agent_id)
        sev = CacheKeyBuilder._normalize_str(severity)
        sev = sev.lower() if sev else None
        parts = {
            'agent': agent or '*',
            'severity': sev
        }
        return {
            'namespace': 'vulnerabilities',
            'parts': parts,
            'key': CacheKeyBuilder._build_key('vulnerabilities', parts)
        }

    @staticmethod
    def processes_key(agent_id: str, include_children: bool = True) -> Dict[str, Any]:
        agent = CacheKeyBuilder._normalize_str(agent_id)
        inc = CacheKeyBuilder._normalize_bool(include_children)
        parts = {
            'agent': agent or '*',
            'children': inc
        }
        return {
            'namespace': 'processes',
            'parts': parts,
            'key': CacheKeyBuilder._build_key('processes', parts)
        }

    @staticmethod
    def ports_key(agent_id: str, state: list[str] = None, protocol: list[str] = None) -> Dict[str, Any]:
        agent = CacheKeyBuilder._normalize_str(agent_id)
        st = CacheKeyBuilder._normalize_list(state)
        proto = CacheKeyBuilder._normalize_list(protocol)
        parts = {
            'agent': agent or '*',
            'state': st,
            'protocol': proto
        }
        return {
            'namespace': 'ports',
            'parts': parts,
            'key': CacheKeyBuilder._build_key('ports', parts)
        }
