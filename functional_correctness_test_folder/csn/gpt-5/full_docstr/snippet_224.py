from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Host:
    name: str
    description: Optional[str] = None
    stats: Dict[str, Any] = field(default_factory=dict)


class HostManager:
    '''
    Functions for managing hosts. Intended to be used as a mixin for CloudManager.
    '''

    def _ensure_host_store(self) -> None:
        if not hasattr(self, "_hosts"):
            self._hosts: Dict[str, Host] = {}

    def get_hosts(self) -> List[Host]:
        '''
        Returns a list of available hosts, along with basic statistics of them when available.
        '''
        self._ensure_host_store()
        return list(self._hosts.values())

    def get_host(self, host: str) -> Host:
        '''
        Returns detailed information about a specific host.
        '''
        self._ensure_host_store()
        try:
            return self._hosts[host]
        except KeyError as e:
            raise KeyError(f"Host not found: {host}") from e

    def modify_host(self, host: str, description: str) -> Host:
        '''
        Modifies description of a specific host.
        '''
        self._ensure_host_store()
        if host not in self._hosts:
            self._hosts[host] = Host(name=host, description=description)
        else:
            self._hosts[host].description = description
        return self._hosts[host]
