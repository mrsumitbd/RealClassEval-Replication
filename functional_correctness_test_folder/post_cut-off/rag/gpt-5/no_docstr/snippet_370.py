from typing import Optional, Tuple, List, Dict, Any
import os
import requests
import uuid


class SimpleRegistryClient:
    """Simple client for querying MCP registries for server discovery."""

    def __init__(self, registry_url: Optional[str] = None):
        """Initialize the registry client.
        Args:
            registry_url (str, optional): URL of the MCP registry.
                If not provided, uses the MCP_REGISTRY_URL environment variable
                or falls back to the default demo registry.
        """
        self.base_url = (registry_url or os.getenv(
            "MCP_REGISTRY_URL") or "https://registry.modelcontextprotocol.io").rstrip("/")
        self._session = requests.Session()
        self._session.headers.update(
            {"Accept": "application/json", "User-Agent": "SimpleRegistryClient/1.0"})
        self._timeout = 15

    def list_servers(self, limit: int = 100, cursor: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """List all available servers in the registry.
        Args:
            limit (int, optional): Maximum number of entries to return. Defaults to 100.
            cursor (str, optional): Pagination cursor for retrieving next set of results.
        Returns:
            Tuple[List[Dict[str, Any]], Optional[str]]: List of server metadata dictionaries and the next cursor if available.
        Raises:
            requests.RequestException: If the request fails.
        """
        params: Dict[str, Any] = {"limit": limit}
        if cursor:
            params["cursor"] = cursor

        data = self._get_json(
            [f"{self.base_url}/v1/servers", f"{self.base_url}/servers"],
            params=params,
        )
        items, next_cursor = self._extract_items_and_cursor(data)
        return items, next_cursor

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        """Search for servers in the registry.
        Args:
            query (str): Search query string.
        Returns:
            List[Dict[str, Any]]: List of matching server metadata dictionaries.
        Raises:
            requests.RequestException: If the request fails.
        """
        params = {"query": query}
        data = self._get_json(
            [
                f"{self.base_url}/v1/servers/search",
                f"{self.base_url}/servers/search",
                # some registries may use a generic search
                f"{self.base_url}/search",
            ],
            params=params,
        )
        items, _ = self._extract_items_and_cursor(data)
        return items

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific server.
        Args:
            server_id (str): ID of the server.
        Returns:
            Dict[str, Any]: Server metadata dictionary.
        Raises:
            requests.RequestException: If the request fails.
            ValueError: If the server is not found.
        """
        try:
            data = self._get_json(
                [
                    f"{self.base_url}/v1/servers/{server_id}",
                    f"{self.base_url}/servers/{server_id}",
                ]
            )
        except requests.HTTPError as e:
            if getattr(e.response, "status_code", None) == 404:
                raise ValueError(f"Server not found: {server_id}") from e
            raise
        if not isinstance(data, dict):
            raise ValueError(
                f"Unexpected server info response format for: {server_id}")
        return data

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a server by its name.
        Args:
            name (str): Name of the server to find.
        Returns:
            Optional[Dict[str, Any]]: Server metadata dictionary or None if not found.
        Raises:
            requests.RequestException: If the request fails.
        """
        # Prefer search if available
        try:
            results = self.search_servers(name)
            for item in results:
                if self._matches_name(item, name):
                    return item
        except requests.RequestException:
            pass

        # Fallback: iterate through listing pages
        cursor: Optional[str] = None
        while True:
            items, cursor = self.list_servers(limit=200, cursor=cursor)
            for item in items:
                if self._matches_name(item, name):
                    return item
            if not cursor:
                break
        return None

    def find_server_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        """Find a server by exact name match or server ID.
        This is a simple, efficient lookup that only makes network requests when necessary:
        1. Server ID (UUID format) - direct API call
        2. Exact name match from server list - single additional API call
        Args:
            reference (str): Server reference (ID or exact name).
        Returns:
            Optional[Dict[str, Any]]: Server metadata dictionary or None if not found.
        Raises:
            requests.RequestException: If the request fails.
        """
        # 1) If it's a UUID-like server ID, get it directly.
        if self._is_uuid(reference):
            try:
                return self.get_server_info(reference)
            except ValueError:
                return None

        # 2) Otherwise iterate server list to find exact name, then fetch full details by ID.
        cursor: Optional[str] = None
        while True:
            items, cursor = self.list_servers(limit=200, cursor=cursor)
            for item in items:
                if self._matches_name(item, reference):
                    server_id = self._extract_id(item)
                    if server_id:
                        try:
                            return self.get_server_info(server_id)
                        except ValueError:
                            return None
                    return item
            if not cursor:
                break
        return None

    def _get_json(self, url_candidates: List[str], params: Optional[Dict[str, Any]] = None) -> Any:
        last_error: Optional[requests.HTTPError] = None
        for url in url_candidates:
            try:
                resp = self._session.get(
                    url, params=params, timeout=self._timeout)
                if resp.status_code == 404:
                    # try next candidate endpoint
                    last_error = requests.HTTPError("Not Found", response=resp)
                    continue
                resp.raise_for_status()
                return resp.json()
            except requests.HTTPError as e:
                # For non-404 errors, raise immediately.
                if getattr(e.response, "status_code", None) != 404:
                    raise
                last_error = e
        if last_error:
            raise last_error
        raise requests.RequestException("No URL candidates provided")

    @staticmethod
    def _extract_items_and_cursor(payload: Any) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        if isinstance(payload, list):
            items = payload
            next_cursor = None
        elif isinstance(payload, dict):
            items = None
            for key in ("servers", "items", "data", "results"):
                if key in payload and isinstance(payload[key], list):
                    items = payload[key]
                    break
            if items is None:
                items = []
            next_cursor = (
                payload.get("next_cursor")
                or payload.get("nextCursor")
                or (payload.get("meta", {}) or {}).get("next_cursor")
                or (payload.get("meta", {}) or {}).get("nextCursor")
            )
        else:
            items = []
            next_cursor = None
        # Ensure dict list
        items = [i for i in items if isinstance(i, dict)]
        return items, next_cursor

    @staticmethod
    def _is_uuid(value: str) -> bool:
        try:
            uuid.UUID(value)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def _matches_name(item: Dict[str, Any], name: str) -> bool:
        target = name.strip().lower()
        candidates = []
        # Common direct keys
        for key in ("name", "displayName", "title"):
            if key in item and isinstance(item[key], str):
                candidates.append(item[key])
        # Nested metadata
        meta = item.get("metadata") or item.get("meta") or {}
        if isinstance(meta, dict):
            for key in ("name", "displayName", "title"):
                val = meta.get(key)
                if isinstance(val, str):
                    candidates.append(val)
        return any(str(c or "").strip().lower() == target for c in candidates)

    @staticmethod
    def _extract_id(item: Dict[str, Any]) -> Optional[str]:
        for key in ("id", "server_id", "serverId", "uuid"):
            val = item.get(key)
            if isinstance(val, str) and val:
                return val
        # Some registries may nest ID in metadata
        meta = item.get("metadata") or item.get("meta") or {}
        if isinstance(meta, dict):
            for key in ("id", "server_id", "serverId", "uuid"):
                val = meta.get(key)
                if isinstance(val, str) and val:
                    return val
        return None
