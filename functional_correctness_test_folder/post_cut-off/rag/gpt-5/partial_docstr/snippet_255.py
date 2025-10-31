from typing import Any, Dict, Optional


class CacheKeyBuilder:
    """Helper class to build standardized cache keys."""

    @staticmethod
    def _build_key(kind: str, **kwargs: Any) -> Dict[str, Any]:
        key: Dict[str, Any] = {"type": kind}
        for k, v in kwargs.items():
            if v is None:
                continue
            if isinstance(v, (list, set, tuple)):
                v = tuple(sorted(v))
            key[k] = v
        return key

    @staticmethod
    def alerts_key(agent_id: Optional[str] = None, time_range: str = "24h", level: Optional[int] = None) -> Dict[str, Any]:
        """Build cache key for alerts."""
        return CacheKeyBuilder._build_key("alerts", agent_id=agent_id, time_range=time_range, level=level)

    @staticmethod
    def agent_health_key(agent_id: str) -> Dict[str, Any]:
        """Build cache key for agent health."""
        return CacheKeyBuilder._build_key("agent_health", agent_id=agent_id)

    @staticmethod
    def vulnerabilities_key(agent_id: Optional[str] = None, severity: Optional[str] = None) -> Dict[str, Any]:
        """Build cache key for vulnerabilities."""
        return CacheKeyBuilder._build_key("vulnerabilities", agent_id=agent_id, severity=severity)

    @staticmethod
    def processes_key(agent_id: str, include_children: bool = True) -> Dict[str, Any]:
        """Build cache key for processes."""
        return CacheKeyBuilder._build_key("processes", agent_id=agent_id, include_children=include_children)

    @staticmethod
    def ports_key(agent_id: str, state: Optional[list[str]] = None, protocol: Optional[list[str]] = None) -> Dict[str, Any]:
        """Build cache key for ports."""
        return CacheKeyBuilder._build_key("ports", agent_id=agent_id, state=state, protocol=protocol)
