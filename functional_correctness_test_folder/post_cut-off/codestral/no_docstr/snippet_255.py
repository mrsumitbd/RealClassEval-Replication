
class CacheKeyBuilder:

    @staticmethod
    def alerts_key(agent_id: Optional[str] = None, time_range: str = '24h', level: Optional[int] = None) -> Dict[str, Any]:

        key = {'type': 'alerts', 'time_range': time_range}
        if agent_id is not None:
            key['agent_id'] = agent_id
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

        return {'type': 'processes', 'agent_id': agent_id, 'include_children': include_children}

    @staticmethod
    def ports_key(agent_id: str, state: list[str] = None, protocol: list[str] = None) -> Dict[str, Any]:

        key = {'type': 'ports', 'agent_id': agent_id}
        if state is not None:
            key['state'] = state
        if protocol is not None:
            key['protocol'] = protocol
        return key
