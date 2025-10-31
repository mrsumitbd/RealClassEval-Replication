from dataclasses import dataclass
from typing import Dict, List, Iterable, Optional


@dataclass
class Host:
    name: str
    description: str = ""


class HostManager:
    def __init__(self, hosts: Optional[Iterable[Host]] = None):
        self._hosts: Dict[str, Host] = {}
        if hosts:
            for h in hosts:
                if not isinstance(h, Host):
                    raise TypeError(
                        "hosts must be an iterable of Host instances")
                self._hosts[h.name] = Host(
                    name=h.name, description=h.description)

    def get_hosts(self):
        return list(self._hosts.values())

    def get_hosts(self):
        return list(self._hosts.values())

    def modify_host(self, host: str, description: str) -> Host:
        '''
        Modifies description of a specific host.
        '''
        if not isinstance(host, str) or not host:
            raise ValueError("host must be a non-empty string")
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        try:
            h = self._hosts[host]
        except KeyError as e:
            raise KeyError(f"Host '{host}' not found") from e
        h.description = description
        return h
