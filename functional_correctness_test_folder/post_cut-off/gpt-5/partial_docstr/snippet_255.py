from typing import Optional, Dict, Any, Iterable


class CacheKeyBuilder:
    '''Helper class to build standardized cache keys.'''

    _VERSION = 1

    @staticmethod
    def _validate_agent_id(agent_id: Optional[str], required: bool = False) -> Optional[str]:
        if agent_id is None:
            if required:
                raise ValueError("agent_id is required")
            return None
        if not isinstance(agent_id, str):
            raise TypeError("agent_id must be a string")
        aid = agent_id.strip()
        if required and not aid:
            raise ValueError("agent_id cannot be empty")
        return aid or None

    @staticmethod
    def _norm_str(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError("value must be a string")
        v = value.strip()
        return v or None

    @staticmethod
    def _norm_int(value: Optional[int]) -> Optional[int]:
        if value is None:
            return None
        if not isinstance(value, int):
            raise TypeError("value must be an int")
        return value

    @staticmethod
    def _norm_bool(value: Optional[bool]) -> Optional[bool]:
        if value is None:
            return None
        if not isinstance(value, bool):
            raise TypeError("value must be a bool")
        return value

    @staticmethod
    def _norm_list(values: Optional[Iterable[str]], lower: bool = True) -> Optional[list]:
        if values is None:
            return None
        if isinstance(values, str):
            raise TypeError(
                "values must be an iterable of strings, not a string")
        normed = []
        for v in values:
            if v is None:
                continue
            if not isinstance(v, str):
                raise TypeError("list values must be strings")
            s = v.strip()
            if not s:
                continue
            normed.append(s.lower() if lower else s)
        if not normed:
            return None
        # unique and sorted for stability
        return sorted(set(normed))

    @staticmethod
    def _clean_params(params: Dict[str, Any]) -> Dict[str, Any]:
        return {k: v for k, v in params.items() if v is not None}

    @staticmethod
    def _build(namespace: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "namespace": namespace,
            "version": CacheKeyBuilder._VERSION,
            "params": CacheKeyBuilder._clean_params(params),
        }

    @staticmethod
    def alerts_key(agent_id: Optional[str] = None, time_range: str = '24h', level: Optional[int] = None) -> Dict[str, Any]:
        '''Build cache key for alerts.'''
        aid = CacheKeyBuilder._validate_agent_id(agent_id, required=False)
        tr = CacheKeyBuilder._norm_str(time_range)
        if tr is None:
            raise ValueError("time_range cannot be empty")
        lvl = CacheKeyBuilder._norm_int(level)
        return CacheKeyBuilder._build(
            "alerts",
            {
                "agent_id": aid,
                "time_range": tr,
                "level": lvl,
            },
        )

    @staticmethod
    def agent_health_key(agent_id: str) -> Dict[str, Any]:
        aid = CacheKeyBuilder._validate_agent_id(agent_id, required=True)
        return CacheKeyBuilder._build(
            "agent_health",
            {
                "agent_id": aid,
            },
        )

    @staticmethod
    def vulnerabilities_key(agent_id: Optional[str] = None, severity: Optional[str] = None) -> Dict[str, Any]:
        aid = CacheKeyBuilder._validate_agent_id(agent_id, required=False)
        sev = CacheKeyBuilder._norm_str(severity)
        sev = sev.lower() if sev is not None else None
        return CacheKeyBuilder._build(
            "vulnerabilities",
            {
                "agent_id": aid,
                "severity": sev,
            },
        )

    @staticmethod
    def processes_key(agent_id: str, include_children: bool = True) -> Dict[str, Any]:
        '''Build cache key for processes.'''
        aid = CacheKeyBuilder._validate_agent_id(agent_id, required=True)
        inc = CacheKeyBuilder._norm_bool(include_children)
        return CacheKeyBuilder._build(
            "processes",
            {
                "agent_id": aid,
                "include_children": inc,
            },
        )

    @staticmethod
    def ports_key(agent_id: str, state: list[str] = None, protocol: list[str] = None) -> Dict[str, Any]:
        '''Build cache key for ports.'''
        aid = CacheKeyBuilder._validate_agent_id(agent_id, required=True)
        st = CacheKeyBuilder._norm_list(state, lower=True)
        proto = CacheKeyBuilder._norm_list(protocol, lower=True)
        return CacheKeyBuilder._build(
            "ports",
            {
                "agent_id": aid,
                "state": st,
                "protocol": proto,
            },
        )
