
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Host:
    """Represents a host with optional statistics."""
    id: str
    description: str = ""
    stats: Dict[str, float] = field(default_factory=dict)


class HostManager:
    """
    Functions for managing hosts. Intended to be used as a mixin for CloudManager.
    """

    def __init__(self) -> None:
        # In‑memory store of hosts keyed by host id
        self._hosts: Dict[str, Host] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get_hosts(self) -> List[Host]:
        """
        Returns a list of available hosts, along with basic statistics of them when available.
        """
        return list(self._hosts.values())

    def get_host(self, host_id: str) -> Optional[Host]:
        """
        Returns detailed information about a specific host.
        """
        return self._hosts.get(host_id)

    def modify_host(self, host_id: str, description: str) -> Host:
        """
        Modifies description of a specific host.
        """
        host = self._hosts.get(host_id)
        if host is None:
            raise KeyError(f"Host '{host_id}' not found")
        host.description = description
        return host

    # ------------------------------------------------------------------
    # Helper methods for demo / testing
    # ------------------------------------------------------------------
    def add_host(self, host_id: str, description: str = "", stats: Optional[Dict[str, float]] = None) -> Host:
        """
        Adds a new host to the manager. This method is not part of the original
        specification but is useful for testing and demonstration.
        """
        if host_id in self._hosts:
            raise KeyError(f"Host '{host_id}' already exists")
        host = Host(id=host_id, description=description, stats=stats or {})
        self._hosts[host_id] = host
        return host

    def remove_host(self, host_id: str) -> None:
        """
        Removes a host from the manager. This method is not part of the original
        specification but is useful for testing and demonstration.
        """
        if host_id not in self._hosts:
            raise KeyError(f"Host '{host_id}' not found")
        del self._hosts[host_id]
