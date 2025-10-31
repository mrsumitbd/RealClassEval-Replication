
from typing import Any, Dict, List, Optional


class CacheKeyBuilder:
    '''Helper class to build standardized cache keys.'''

    @staticmethod
    def _join_parts(parts: List[str]) -> str:
        """Join non-empty parts with ':'."""
        return ':'.join(part for part in parts if part)

    @staticmethod
    def alerts_key(agent_id: Optional[str] = None, time_range: str = '24h', level: Optional[int] = None) -> Dict[str, Any]:
        '''Build cache key for alerts.'''
        parts = ['alerts']
        if agent_id:
            parts.append(agent_id)
        parts.append(time_range)
        if level is not None:
            parts.append(str(level))
        key = CacheKeyBuilder._join_parts(parts)
        return {'key': key}

    @staticmethod
    def agent_health_key(agent_id: str) -> Dict[str, Any]:
        '''Build cache key for agent health.'''
        key = f'agent_health:{agent_id}'
        return {'key': key}

    @staticmethod
    def vulnerabilities_key(agent_id: Optional[str] = None, severity: Optional[str] = None) -> Dict[str, Any]:
        '''Build cache key for vulnerabilities.'''
        parts = ['vulnerabilities']
        if agent_id:
            parts.append(agent_id)
        if severity:
            parts.append(severity)
        key = CacheKeyBuilder._join_parts(parts)
        return {'key': key}

    @staticmethod
    def processes_key(agent_id: str, include_children: bool = True) -> Dict[str, Any]:
        '''Build cache key for processes.'''
        include_str = 'with_children' if include_children else 'no_children'
        key = f'processes:{agent_id}:{include_str}'
        return {'key': key}

    @staticmethod
    def ports_key(agent_id: str, state: List[str] = None, protocol: List[str] = None) -> Dict[str, Any]:
        '''Build cache key for ports.'''
        parts = ['ports', agent_id]
        if state:
            parts.append(','.join(sorted(state)))
        if protocol:
            parts.append(','.join(sorted(protocol)))
        key = CacheKeyBuilder._join_parts(parts)
        return {'key': key}
