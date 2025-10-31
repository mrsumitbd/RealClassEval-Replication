from typing import Dict, Any, Optional, Tuple

class CacheKeyBuilder:
    """Helper class to build standardized cache keys."""

    @staticmethod
    def alerts_key(agent_id: Optional[str]=None, time_range: str='24h', level: Optional[int]=None) -> Dict[str, Any]:
        """Build cache key for alerts."""
        return {'agent_id': agent_id, 'time_range': time_range, 'level': level}

    @staticmethod
    def agent_health_key(agent_id: str) -> Dict[str, Any]:
        """Build cache key for agent health."""
        return {'agent_id': agent_id}

    @staticmethod
    def vulnerabilities_key(agent_id: Optional[str]=None, severity: Optional[str]=None) -> Dict[str, Any]:
        """Build cache key for vulnerabilities."""
        return {'agent_id': agent_id, 'severity': severity}

    @staticmethod
    def processes_key(agent_id: str, include_children: bool=True) -> Dict[str, Any]:
        """Build cache key for processes."""
        return {'agent_id': agent_id, 'include_children': include_children}

    @staticmethod
    def ports_key(agent_id: str, state: list[str]=None, protocol: list[str]=None) -> Dict[str, Any]:
        """Build cache key for ports."""
        return {'agent_id': agent_id, 'state': sorted(state) if state else None, 'protocol': sorted(protocol) if protocol else None}