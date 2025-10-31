from typing import Any, Dict, Iterable, Optional


class CacheKeyBuilder:
    """Helper class to build standardized cache keys."""

    VERSION = 1

    @staticmethod
    def _normalize_str_list(values: Optional[Iterable[str]]) -> tuple:
        if values is None:
            return tuple()
        normalized = {str(v).strip().lower() for v in values if v is not None}
        return tuple(sorted(normalized))

    @staticmethod
    def _key(kind: str, agent_id: Optional[str], params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'version': CacheKeyBuilder.VERSION,
            'type': kind,
            'agent_id': agent_id if agent_id else None,
            'params': params,
        }

    @staticmethod
    def alerts_key(agent_id: Optional[str] = None, time_range: str = '24h', level: Optional[int] = None) -> Dict[str, Any]:
        """Build cache key for alerts."""
        params = {
            'time_range': str(time_range),
            'level': int(level) if level is not None else None,
        }
        return CacheKeyBuilder._key('alerts', agent_id, params)

    @staticmethod
    def agent_health_key(agent_id: str) -> Dict[str, Any]:
        """Build cache key for agent health."""
        return CacheKeyBuilder._key('agent_health', agent_id, params={})

    @staticmethod
    def vulnerabilities_key(agent_id: Optional[str] = None, severity: Optional[str] = None) -> Dict[str, Any]:
        """Build cache key for vulnerabilities."""
        params = {
            'severity': severity.strip().lower() if isinstance(severity, str) else None,
        }
        return CacheKeyBuilder._key('vulnerabilities', agent_id, params)

    @staticmethod
    def processes_key(agent_id: str, include_children: bool = True) -> Dict[str, Any]:
        """Build cache key for processes."""
        params = {
            'include_children': bool(include_children),
        }
        return CacheKeyBuilder._key('processes', agent_id, params)

    @staticmethod
    def ports_key(agent_id: str, state: list[str] = None, protocol: list[str] = None) -> Dict[str, Any]:
        """Build cache key for ports."""
        params = {
            'state': CacheKeyBuilder._normalize_str_list(state),
            'protocol': CacheKeyBuilder._normalize_str_list(protocol),
        }
        return CacheKeyBuilder._key('ports', agent_id, params)
