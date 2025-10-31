from typing import Any, Dict, Optional, Iterable, List


class CacheKeyBuilder:
    """Helper class to build standardized cache keys."""
    _VERSION = 1

    @staticmethod
    def _normalize_str(value: Optional[str]) -> str:
        if value is None:
            return '*'
        v = str(value).strip()
        return v.lower() if v else '*'

    @staticmethod
    def _normalize_time_range(value: Optional[str]) -> str:
        if value is None:
            return '24h'
        v = str(value).strip()
        return v.lower() if v else '24h'

    @staticmethod
    def _normalize_list(values: Optional[Iterable[str]]) -> List[str]:
        if not values:
            return ['*']
        cleaned = {str(v).strip().lower()
                   for v in values if v is not None and str(v).strip()}
        return sorted(cleaned) if cleaned else ['*']

    @staticmethod
    def _require_agent_id(agent_id: Optional[str]) -> str:
        if not agent_id or not str(agent_id).strip():
            raise ValueError('agent_id is required')
        return str(agent_id).strip()

    @staticmethod
    def _key(resource: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {'v': CacheKeyBuilder._VERSION, 'resource': resource, 'params': params}

    @staticmethod
    def alerts_key(agent_id: Optional[str] = None, time_range: str = '24h', level: Optional[int] = None) -> Dict[str, Any]:
        """Build cache key for alerts."""
        params: Dict[str, Any] = {
            'agent_id': CacheKeyBuilder._normalize_str(agent_id),
            'time_range': CacheKeyBuilder._normalize_time_range(time_range),
            'level': level if level is not None else '*',
        }
        return CacheKeyBuilder._key('alerts', params)

    @staticmethod
    def agent_health_key(agent_id: str) -> Dict[str, Any]:
        """Build cache key for agent health."""
        agent_id = CacheKeyBuilder._require_agent_id(agent_id)
        return CacheKeyBuilder._key('agent_health', {'agent_id': agent_id})

    @staticmethod
    def vulnerabilities_key(agent_id: Optional[str] = None, severity: Optional[str] = None) -> Dict[str, Any]:
        """Build cache key for vulnerabilities."""
        params: Dict[str, Any] = {
            'agent_id': CacheKeyBuilder._normalize_str(agent_id),
            'severity': CacheKeyBuilder._normalize_str(severity),
        }
        return CacheKeyBuilder._key('vulnerabilities', params)

    @staticmethod
    def processes_key(agent_id: str, include_children: bool = True) -> Dict[str, Any]:
        """Build cache key for processes."""
        agent_id = CacheKeyBuilder._require_agent_id(agent_id)
        params: Dict[str, Any] = {
            'agent_id': agent_id,
            'include_children': bool(include_children),
        }
        return CacheKeyBuilder._key('processes', params)

    @staticmethod
    def ports_key(agent_id: str, state: list[str] = None, protocol: list[str] = None) -> Dict[str, Any]:
        """Build cache key for ports."""
        agent_id = CacheKeyBuilder._require_agent_id(agent_id)
        params: Dict[str, Any] = {
            'agent_id': agent_id,
            'state': CacheKeyBuilder._normalize_list(state),
            'protocol': CacheKeyBuilder._normalize_list(protocol),
        }
        return CacheKeyBuilder._key('ports', params)
