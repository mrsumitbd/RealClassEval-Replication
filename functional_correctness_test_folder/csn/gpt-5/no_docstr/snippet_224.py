from dataclasses import dataclass
from typing import Dict, List, Optional
from threading import RLock


@dataclass(frozen=True)
class Host:
    name: str
    description: str = ""


class HostManager:
    def __init__(self, initial_hosts: Optional[List[Host]] = None):
        self._hosts: Dict[str, Host] = {}
        self._lock = RLock()
        if initial_hosts:
            for h in initial_hosts:
                if not h.name:
                    continue
                self._hosts[h.name] = h

    def get_hosts(self) -> List[Host]:
        with self._lock:
            return sorted(self._hosts.values(), key=lambda h: h.name)

    def modify_host(self, host: str, description: str) -> Host:
        if host is None:
            raise ValueError("host cannot be None")
        host_name = host.strip()
        if not host_name:
            raise ValueError("host cannot be empty or whitespace")
        desc = description if description is not None else ""
        with self._lock:
            new_host = Host(name=host_name, description=desc)
            self._hosts[host_name] = new_host
            return new_host
