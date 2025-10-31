from typing import Any, Dict, Optional


class CacheKeyBuilder:

    @staticmethod
    def _normalize_list(values: Optional[list[str]]) -> Optional[list[str]]:
        if values is None:
            return None
        # Remove Nones, cast to str, lower, unique, sorted
        normalized = sorted({str(v).lower() for v in values if v is not None})
        return normalized

    @staticmethod
    def _build_key(namespace: str, **kwargs: Any) -> Dict[str, Any]:
        key: Dict[str, Any] = {"namespace": namespace}
        for k, v in kwargs.items():
            if v is None:
                continue
            if isinstance(v, list):
                norm = CacheKeyBuilder._normalize_list(v)
                if norm is None:
                    continue
                key[k] = norm
            else:
                key[k] = v
        return key

    @staticmethod
    def alerts_key(agent_id: Optional[str] = None, time_range: str = '24h', level: Optional[int] = None) -> Dict[str, Any]:
        return CacheKeyBuilder._build_key(
            "alerts",
            agent_id=agent_id,
            time_range=str(time_range),
            level=level,
        )

    @staticmethod
    def agent_health_key(agent_id: str) -> Dict[str, Any]:
        return CacheKeyBuilder._build_key(
            "agent_health",
            agent_id=agent_id,
        )

    @staticmethod
    def vulnerabilities_key(agent_id: Optional[str] = None, severity: Optional[str] = None) -> Dict[str, Any]:
        sev = severity.lower() if isinstance(severity, str) else None
        return CacheKeyBuilder._build_key(
            "vulnerabilities",
            agent_id=agent_id,
            severity=sev,
        )

    @staticmethod
    def processes_key(agent_id: str, include_children: bool = True) -> Dict[str, Any]:
        return CacheKeyBuilder._build_key(
            "processes",
            agent_id=agent_id,
            include_children=bool(include_children),
        )

    @staticmethod
    def ports_key(agent_id: str, state: list[str] = None, protocol: list[str] = None) -> Dict[str, Any]:
        return CacheKeyBuilder._build_key(
            "ports",
            agent_id=agent_id,
            state=state,
            protocol=protocol,
        )
