from typing import Optional, Tuple, List, Dict, Any
import os
import re
import requests


class SimpleRegistryClient:
    '''Simple client for querying MCP registries for server discovery.'''

    DEFAULT_REGISTRY_URL = "https://registry.modelcontextprotocol.io"

    def __init__(self, registry_url: Optional[str] = None):
        '''Initialize the registry client.
        Args:
            registry_url (str, optional): URL of the MCP registry.
                If not provided, uses the MCP_REGISTRY_URL environment variable
                or falls back to the default demo registry.
        '''
        self.base_url = (registry_url or os.getenv(
            "MCP_REGISTRY_URL") or self.DEFAULT_REGISTRY_URL).rstrip("/")
        self.timeout = 15

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}{path}"
        resp = requests.get(url, params=params or {}, timeout=self.timeout)
        if resp.status_code == 404:
            # Allow callers to distinguish 404 if needed
            raise requests.HTTPError("Not found", response=resp)
        resp.raise_for_status()
        ct = resp.headers.get("Content-Type", "")
        if "application/json" in ct or resp.text.strip().startswith(("{", "[")):
            return resp.json()
        return resp.text

    @staticmethod
    def _extract_items_and_cursor(payload: Any) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        if isinstance(payload, dict):
            # Common shapes
            items = payload.get("items")
            if items is None:
                items = payload.get("servers")
            if items is None and "data" in payload and isinstance(payload["data"], list):
                items = payload["data"]
            if items is None:
                items = []

            next_cursor = (
                payload.get("next_cursor")
                or payload.get("next")
                or payload.get("cursor")
                or None
            )
            if isinstance(next_cursor, dict):
                next_cursor = next_cursor.get("cursor") or None

            return list(items), next_cursor
        if isinstance(payload, list):
            return list(payload), None
        return [], None

    def list_servers(self, limit: int = 100, cursor: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        params: Dict[str, Any] = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        payload = self._get("/servers", params=params)
        items, next_cursor = self._extract_items_and_cursor(payload)
        return items, next_cursor

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        '''Search for servers in the registry.
        Args:
            query (str): Search query string.
        Returns:
            List[Dict[str, Any]]: List of matching server metadata dictionaries.
        Raises:
            requests.RequestException: If the request fails.
        '''
        q = (query or "").strip()
        if not q:
            return []
        payload = self._get("/servers/search", params={"q": q})
        items, _ = self._extract_items_and_cursor(payload)
        return items

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        '''Get detailed information about a specific server.
        Args:
            server_id (str): ID of the server.
        Returns:
            Dict[str, Any]: Server metadata dictionary.
        Raises:
            requests.RequestException: If the request fails.
            ValueError: If the server is not found.
        '''
        try:
            payload = self._get(f"/servers/{server_id}")
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                raise ValueError(f"Server not found: {server_id}") from e
            raise
        if not isinstance(payload, dict):
            raise ValueError("Unexpected response format")
        return payload

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        qname = (name or "").strip()
        if not qname:
            return None
        results = self.search_servers(qname)
        for item in results:
            if isinstance(item, dict) and item.get("name") == qname:
                return item
        return None

    def find_server_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        '''Find a server by exact name match or server ID.
        This is a simple, efficient lookup that only makes network requests when necessary:
        1. Server ID (UUID format) - direct API call
        2. Exact name match from server list - single additional API call
        Args:
            reference (str): Server reference (ID or exact name).
        Returns:
            Optional[Dict[str, Any]]: Server metadata dictionary or None if not found.
        Raises:
            requests.RequestException: If the request fails.
        '''
        ref = (reference or "").strip()
        if not ref:
            return None

        uuid_re = re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        )
        if uuid_re.match(ref):
            try:
                return self.get_server_info(ref)
            except ValueError:
                return None

        return self.get_server_by_name(ref)
