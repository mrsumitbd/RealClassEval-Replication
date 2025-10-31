
import json
import requests
from typing import Any, Dict, List, Optional, Union


class XinyuSearchAPI:
    """
    A lightweight wrapper around the Xinyu Search API.

    Parameters
    ----------
    access_key : str
        API key used for authentication.
    search_engine_id : str
        Identifier of the search engine to use.
    max_results : int, default 20
        Default maximum number of results to return for a search.
    """

    BASE_URL = "https://api.xinyu.com"

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        if not access_key:
            raise ValueError("access_key must be provided")
        if not search_engine_id:
            raise ValueError("search_engine_id must be provided")
        if max_results <= 0:
            raise ValueError("max_results must be a positive integer")

        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.access_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _handle_response(self, resp: requests.Response) -> List[Dict[str, Any]]:
        try:
            resp.raise_for_status()
        except requests.HTTPError as exc:
            # Try to extract error message from JSON
            try:
                error_info = resp.json()
                msg = error_info.get("error", str(error_info))
            except Exception:
                msg = resp.text or str(exc)
            raise RuntimeError(f"API request failed: {msg}") from exc

        try:
            data = resp.json()
        except json.JSONDecodeError as exc:
            raise RuntimeError("Failed to parse JSON response") from exc

        # The API is expected to return a list of result objects
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "results" in data:
            return data["results"]
        raise RuntimeError("Unexpected API response format")

    def query_detail(self, body: Optional[Dict[str, Any]] = None, detail: bool = True) -> List[Dict[str, Any]]:
        """
        Retrieve detailed information for a specific query.

        Parameters
        ----------
        body : dict, optional
            Payload to send with the request. If omitted, an empty payload is sent.
        detail : bool, default True
            Whether to request detailed information. This flag is sent as a query parameter.

        Returns
        -------
        list[dict]
            A list of detailed result objects.
        """
        url = f"{self.BASE_URL}/detail"
        params = {"detail": str(detail).lower()}
        payload = body or {}

        try:
            resp = self.session.post(
                url, params=params, json=payload, timeout=10)
        except requests.RequestException as exc:
            raise RuntimeError(
                f"Network error during query_detail: {exc}") from exc

        return self._handle_response(resp)

    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Perform a search query.

        Parameters
        ----------
        query : str
            The search string.
        max_results : int, optional
            Override the default maximum number of results.

        Returns
        -------
        list[dict]
            A list of search result objects.
        """
        if not query:
            raise ValueError("query must be a non-empty string")

        url = f"{self.BASE_URL}/search"
        params = {
            "q": query,
            "engine_id": self.search_engine_id,
            "limit": max_results if max_results is not None else self.max_results,
        }

        try:
            resp = self.session.get(url, params=params, timeout=10)
        except requests.RequestException as exc:
            raise RuntimeError(f"Network error during search: {exc}") from exc

        return self._handle_response(resp)
