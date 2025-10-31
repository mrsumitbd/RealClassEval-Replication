
from typing import Optional, Dict, Any, List


class CacheKeyBuilder:

    @staticmethod
    def alerts_key(agent_id: Optional[str] = None, time_range: str = '24h', level: Optional[int] = None) -> Dict[str, Any]:
        return {
            "type": "alerts",
            "agent_id": agent_id,
            "time_range": time_range,
            "level": level
        }

    @staticmethod
    def agent_health_key(agent_id: str) -> Dict[str, Any]:
        return {
            "type": "agent_health",
            "agent_id": agent_id
        }

    @staticmethod
    def vulnerabilities_key(agent_id: Optional[str] = None, severity: Optional[str] = None) -> Dict[str, Any]:
        return {
            "type": "vulnerabilities",
            "agent_id": agent_id,
            "severity": severity
        }

    @staticmethod
    def processes_key(agent_id: str, include_children: bool = True) -> Dict[str, Any]:
        return {
            "type": "processes",
            "agent_id": agent_id,
            "include_children": include_children
        }

    @staticmethod
    def ports_key(agent_id: str, state: Optional[List[str]] = None, protocol: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            "type": "ports",
            "agent_id": agent_id,
            "state": state if state is not None else [],
            "protocol": protocol if protocol is not None else []
        }
