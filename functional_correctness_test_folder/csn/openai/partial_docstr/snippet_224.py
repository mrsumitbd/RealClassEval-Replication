
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Host:
    """Simple representation of a host."""
    host: str
    description: str


class HostManager:
    """Manages a collection of Host objects in memory."""

    def __init__(self) -> None:
        # Internal storage: mapping from host name to Host instance
        self._hosts: Dict[str, Host] = {}

    def get_hosts(self) -> List[Host]:
        """
        Return a list of all Host objects managed by this instance.
        """
        return list(self._hosts.values())

    def modify_host(self, host: str, description: str) -> Host:
        """
        Modify the description of a specific host.

        Parameters
        ----------
        host : str
            The identifier of the host to modify.
        description : str
            The new description for the host.

        Returns
        -------
        Host
            The updated Host object.

        Raises
        ------
        KeyError
            If the host does not exist in the manager.
        """
        if host not in self._hosts:
            raise KeyError(f"Host '{host}' not found.")
        self._hosts[host].description = description
        return self._hosts[host]

    # Optional helper methods for completeness

    def add_host(self, host: str, description: str) -> Host:
        """
        Add a new host to the manager.

        Parameters
        ----------
        host : str
            The identifier of the new host.
        description : str
            The description for the new host.

        Returns
        -------
        Host
            The newly created Host object.

        Raises
        ------
        ValueError
            If the host already exists.
        """
        if host in self._hosts:
            raise ValueError(f"Host '{host}' already exists.")
        new_host = Host(host=host, description=description)
        self._hosts[host] = new_host
        return new_host

    def remove_host(self, host: str) -> None:
        """
        Remove a host from the manager.

        Parameters
        ----------
        host : str
            The identifier of the host to remove.

        Raises
        ------
        KeyError
            If the host does not exist.
        """
        if host not in self._hosts:
            raise KeyError(f"Host '{host}' not found.")
        del self._hosts[host]
