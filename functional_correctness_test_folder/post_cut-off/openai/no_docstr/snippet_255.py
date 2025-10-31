
from typing import Any, Dict, List, Optional


class CacheKeyBuilder:
    @staticmethod
    def alerts_key(agent_id: Optional[str] = None, time_range: str = "24h", level: Optional[int] = None) -> Dict[str, Any]:
        """
        Build a cache key dictionary for alerts.

        Parameters
        ----------
        agent_id : Optional[str]
            Identifier of the agent. If None, the key will not include an agent filter.
        time_range : str
            Time range filter for alerts. Defaults to "24h".
        level : Optional[int]
            Severity level filter for alerts. If None, no level filter is applied.

        Returns
        -------
        Dict[str, Any]
            Dictionary representing the cache key.
        """
        key: Dict[str, Any] = {"type": "alerts", "time_range": time_range}
        if agent_id is not None:
            key["agent_id"] = agent_id
        if level is not None:
            key["level"] = level
        return key

    @staticmethod
    def agent_health_key(agent_id: str) -> Dict[str, Any]:
        """
        Build a cache key dictionary for agent health.

        Parameters
        ----------
        agent_id : str
            Identifier of the agent.

        Returns
        -------
        Dict[str, Any]
            Dictionary representing the cache key.
        """
        return {"type": "agent_health", "agent_id": agent_id}

    @staticmethod
    def vulnerabilities_key(agent_id: Optional[str] = None, severity: Optional[str] = None) -> Dict[str, Any]:
        """
        Build a cache key dictionary for vulnerabilities.

        Parameters
        ----------
        agent_id : Optional[str]
            Identifier of the agent. If None, the key will not include an agent filter.
        severity : Optional[str]
            Severity filter for vulnerabilities. If None, no severity filter is applied.

        Returns
        -------
        Dict[str, Any]
            Dictionary representing the cache key.
        """
        key: Dict[str, Any] = {"type": "vulnerabilities"}
        if agent_id is not None:
            key["agent_id"] = agent_id
        if severity is not None:
            key["severity"] = severity
        return key

    @staticmethod
    def processes_key(agent_id: str, include_children: bool = True) -> Dict[str, Any]:
        """
        Build a cache key dictionary for processes.

        Parameters
        ----------
        agent_id : str
            Identifier of the agent.
        include_children : bool
            Whether to include child processes in the cache key.

        Returns
        -------
        Dict[str, Any]
            Dictionary representing the cache key.
        """
        return {
            "type": "processes",
            "agent_id": agent_id,
            "include_children": include_children,
        }

    @staticmethod
    def ports_key(agent_id: str, state: Optional[List[str]] = None, protocol: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Build a cache key dictionary for ports.

        Parameters
        ----------
        agent_id : str
            Identifier of the agent.
        state : Optional[List[str]]
            List of port states to filter by. If None, no state filter is applied.
        protocol : Optional[List[str]]
            List of protocols to filter by. If None, no protocol filter is applied.

        Returns
        -------
        Dict[str, Any]
            Dictionary representing the cache key.
        """
        key: Dict[str, Any] = {"type": "ports", "agent_id": agent_id}
        if state is not None:
            key["state"] = state
        if protocol is not None:
            key["protocol"] = protocol
        return key
