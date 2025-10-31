
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Host:
    host: str
    description: str = ""


class HostManager:
    def __init__(self):
        self._hosts: List[Host] = []

    def get_hosts(self) -> List[Host]:
        """Return a copy of the list of hosts."""
        return list(self._hosts)

    def add_host(self, host: str, description: str = "") -> Host:
        """Add a new host to the manager."""
        new_host = Host(host=host, description=description)
        self._hosts.append(new_host)
        return new_host

    def modify_host(self, host: str, description: str) -> Host:
        """Modify the description of an existing host."""
        for h in self._hosts:
            if h.host == host:
                h.description = description
                return h
        raise ValueError(f"Host '{host}' not found.")
