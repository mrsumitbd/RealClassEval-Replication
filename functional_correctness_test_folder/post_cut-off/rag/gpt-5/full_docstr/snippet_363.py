from typing import Optional, Tuple, List, Dict, Any
import os
import re
import requests


class SimpleRegistryClient:
    """Simple client for querying MCP registries for server discovery."""

    DEFAULT_REGISTRY_URL = "https://registry.modelcontextprotocol.io"
    DEFAULT_TIMEOUT = 10

    def __init__(self, registry_url: Optional[str] = None):
        """Initialize the registry client.
        Args:
            registry_url (str, optional): URL of the MCP registry.
                If not provided, uses the MCP_REGISTRY_URL environment variable
                or falls back to the default demo registry.
        """
        base = registry_url or os.getenv(
            "MCP_REGISTRY_URL") or self.DEFAULT_REGISTRY_URL
        self.base_url = self._normalize_base_url(base)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "SimpleRegistryClient/1.0",
            }
        )
        self.timeout = self.DEFAULT_TIMEOUT

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
        url = f"{self.base_url}/v1/servers"
        params: Dict[str, Any] = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        resp = self.session.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        payload = self._safe_json(resp)
        items = self._extract_items(payload)
        next_cursor = self._extract_next_cursor(payload)
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
        url = f"{self.base_url}/v1/servers/search"
        # Prefer 'query' param; some registries might accept 'q' as well.
        params = {"query": query}
        try:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            if resp.status_code == 404:
                # Fallback if search endpoint not supported: fetch list and filter locally.
                return self._fallback_search(query)
            resp.raise_for_status()
            payload = self._safe_json(resp)
            return self._extract_items(payload)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                return self._fallback_search(query)
            raise

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
        url = f"{self.base_url}/v1/servers/{server_id}"
        resp = self.session.get(url, timeout=self.timeout)
        if resp.status_code == 404:
            raise ValueError(f"Server not found: {server_id}")
        resp.raise_for_status()
        payload = self._safe_json(resp)
        if isinstance(payload, dict):
            if "server" in payload and isinstance(payload["server"], dict):
                return payload["server"]
            if "data" in payload and isinstance(payload["data"], dict):
                return payload["data"]
            if "id" in payload:
                return payload
        raise ValueError("Unexpected server info response format")

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a server by its name.
        Args:
            name (str): Name of the server to find.
        Returns:
            Optional[Dict[str, Any]]: Server metadata dictionary or None if not found.
        Raises:
            requests.RequestException: If the request fails.
        """
        candidates = self.search_servers(name)
        name_lower = name.strip().lower()
        exact = next(
            (
                s
                for s in candidates
                if self._get_server_name(s).lower() == name_lower
            ),
            None,
        )
        if not exact:
            return None
        server_id = self._get_server_id(exact)
        if server_id:
            try:
                return self.get_server_info(server_id)
            except (requests.RequestException, ValueError):
                # Fall back to the matched record if details endpoint fails
                return exact
        return exact

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
        ref = reference.strip()
        if self._is_uuid(ref):
            try:
                return self.get_server_info(ref)
            except (requests.RequestException, ValueError):
                return None

        # Single list call; return the matched record if found.
        servers, _ = self.list_servers(limit=1000)
        ref_lower = ref.lower()
        match = next((s for s in servers if self._get_server_name(
            s).lower() == ref_lower), None)
        if match:
            return match
        return None

    # Helpers

    @staticmethod
    def _normalize_base_url(url: str) -> str:
        return url.rstrip("/")

    @staticmethod
    def _is_uuid(value: str) -> bool:
        uuid_regex = re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        )
        return bool(uuid_regex.match(value))

    @staticmethod
    def _extract_next_cursor(payload: Any) -> Optional[str]:
        if not isinstance(payload, dict):
            return None
        for key in ("next_cursor", "nextCursor", "cursor", "next", "nextPageToken"):
            val = payload.get(key)
            if isinstance(val, str) and val:
                return val
        # Some APIs nest pagination under 'meta'
        meta = payload.get("meta")
        if isinstance(meta, dict):
            for key in ("next_cursor", "nextCursor", "cursor", "next", "nextPageToken"):
                val = meta.get(key)
                if isinstance(val, str) and val:
                    return val
        return None

    @staticmethod
    def _extract_items(payload: Any) -> List[Dict[str, Any]]:
        if isinstance(payload, list):
            return [x for x in payload if isinstance(x, dict)]
        if isinstance(payload, dict):
            for key in ("items", "servers", "results", "data"):
                val = payload.get(key)
                if isinstance(val, list):
                    return [x for x in val if isinstance(x, dict)]
            # Some APIs return a single object for non-list endpoints
            if "id" in payload:
                return [payload]
        return []

    @staticmethod
    def _get_server_name(server: Dict[str, Any]) -> str:
        return str(server.get("name") or server.get("title") or server.get("label") or "").strip()

    @staticmethod
    def _get_server_id(server: Dict[str, Any]) -> Optional[str]:
        sid = server.get("id") or server.get("server_id") or server.get("uuid")
        return str(sid) if sid is not None else None

    def _safe_json(self, resp: requests.Response) -> Any:
        try:
            return resp.json()
        except ValueError:
            # Not JSON; re-raise a helpful error
            resp.raise_for_status()
            raise

    def _fallback_search(self, query: str) -> List[Dict[str, Any]]:
        # Basic client-side filtering as a compatibility fallback
        normalized = query.strip().lower()
        servers, _ = self.list_servers(limit=1000)
        results: List[Dict[str, Any]] = []
        for s in servers:
            haystack = " ".join(
                str(x)
                for x in [
                    s.get("name"),
                    s.get("title"),
                    s.get("description"),
                    s.get("summary"),
                ]
                if x is not None
            ).lower()
            if normalized in haystack:
                results.append(s)
        return results
