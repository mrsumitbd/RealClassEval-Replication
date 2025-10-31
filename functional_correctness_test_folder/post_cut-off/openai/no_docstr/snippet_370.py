
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple

import requests


class SimpleRegistryClient:
    """
    A minimal client for interacting with a registry service.

    The client expects the registry to expose a REST API with the following
    endpoints (the exact URLs may vary, but the patterns are used below):

    - GET /servers?limit=<int>&cursor=<str>          -> list servers
    - GET /servers/search?q=<query>                 -> search servers
    - GET /servers/<server_id>                      -> server details
    - GET /servers?name=<name>                      -> server by name
    - GET /servers?reference=<reference>            -> server by reference
    """

    def __init__(self, registry_url: Optional[str] = None):
        """
        Create a new client.

        Parameters
        ----------
        registry_url : Optional[str]
            Base URL of the registry service. If omitted, a default
            URL is used.
        """
        self.registry_url = (
            registry_url or "https://registry.example.com/api/v1"
        )
        self.session = requests.Session()

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform a GET request and return the parsed JSON.

        Raises
        ------
        requests.HTTPError
            If the request fails.
        """
        url = f"{self.registry_url.rstrip('/')}/{path.lstrip('/')}"
        resp = self.session.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def list_servers(
        self, limit: int = 100, cursor: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        Retrieve a paginated list of servers.

        Parameters
        ----------
        limit : int
            Maximum number of servers to return.
        cursor : Optional[str]
            Pagination cursor from a previous call.

        Returns
        -------
        Tuple[List[Dict[str, Any]], Optional[str]]
            A tuple containing the list of servers and the next cursor
            (or None if there are no more pages).
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        data = self._get("/servers", params=params)
        servers = data.get("servers", [])
        next_cursor = data.get("next_cursor")
        return servers, next_cursor

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for servers matching a query string.

        Parameters
        ----------
        query : str
            Search query.

        Returns
        -------
        List[Dict[str, Any]]
            List of matching servers.
        """
        params = {"q": query}
        data = self._get("/servers/search", params=params)
        return data.get("servers", [])

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        """
        Retrieve detailed information for a specific server.

        Parameters
        ----------
        server_id : str
            Identifier of the server.

        Returns
        -------
        Dict[str, Any]
            Server details.

        Raises
        ------
        KeyError
            If the server is not found.
        """
        data = self._get(f"/servers/{server_id}")
        if not data:
            raise KeyError(f"Server {server_id} not found")
        return data

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a server by its name.

        Parameters
        ----------
        name : str
            Name of the server.

        Returns
        -------
        Optional[Dict[str, Any]]
            Server details if found, otherwise None.
        """
        params = {"name": name}
        data = self._get("/servers", params=params)
        servers = data.get("servers", [])
        return servers[0] if servers else None

    def find_server_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a server by a reference string.

        Parameters
        ----------
        reference : str
            Reference identifier.

        Returns
        -------
        Optional[Dict[str, Any]]
            Server details if found, otherwise None.
        """
        params = {"reference": reference}
        data = self._get("/servers", params=params)
        servers = data.get("servers", [])
        return servers[0] if servers else None
