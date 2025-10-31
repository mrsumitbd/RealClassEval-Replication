
from typing import Optional, Dict, Any


class CacheKeyBuilder:
    '''Helper class to build standardized cache keys.'''
    @staticmethod
    def alerts_key(agent_id: Optional[str] = None, time_range: str = '24h', level: Optional[int] = None) -> Dict[str, Any]:
        '''Build cache key for alerts.'''
        key = {'type': 'alerts'}
        if agent_id is not None:
            key['agent_id'] = agent_id
        key['time_range'] = time_range
        if level is not None:
            key['level'] = level
        return key

    @staticmethod
    def agent_health_key(agent_id: str) -> Dict[str, Any]:
        return {'type': 'agent_health', 'agent_id': agent_id}

    @staticmethod
    def vulnerabilities_key(agent_id: Optional[str] = None, severity: Optional[str] = None) -> Dict[str, Any]:
        key = {'type': 'vulnerabilities'}
        if agent_id is not None:
            key['agent_id'] = agent_id
        if severity is not None:
            key['severity'] = severity
        return key

    @staticmethod
    def processes_key(agent_id: str, include_children: bool = True) -> Dict[str, Any]:
        '''Build cache key for processes.'''
        key = {'type': 'processes', 'agent_id': agent_id}
        key['include_children'] = include_children
        return key

    @staticmethod
    def ports_key(agent_id: str, state: list[str] = None, protocol: list[str] = None) -> Dict[str, Any]:
        '''Build cache key for ports.'''
        key = {'type': 'ports', 'agent_id': agent_id}
        if state is not None:
            key['state'] = tuple(sorted(state))
        if protocol is not None:
            key['protocol'] = tuple(sorted(protocol))
        return key
