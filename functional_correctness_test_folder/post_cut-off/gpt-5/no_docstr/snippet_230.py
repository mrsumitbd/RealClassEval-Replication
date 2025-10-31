from typing import List, Dict, Any, Optional
import os
import requests


class TavilySearchService:
    SEARCH_URL = "https://api.tavily.com/search"
    EXTRACT_URL = "https://api.tavily.com/extract"

    def __init__(self):
        self.api_key: Optional[str] = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "TAVILY_API_KEY environment variable is not set.")
        self._session = requests.Session()
        self._timeout = 30

    def search(
        self,
        query: str,
        search_depth: str = "basic",
        topic: str = "general",
        include_domains: List[str] | None = None,
        exclude_domains: List[str] | None = None,
        max_results: int = 5,
    ) -> Dict[str, Any]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string.")
        if search_depth not in {"basic", "advanced"}:
            raise ValueError("search_depth must be 'basic' or 'advanced'.")
        if topic not in {"general", "news"}:
            raise ValueError("topic must be 'general' or 'news'.")
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("max_results must be a positive integer.")
        payload: Dict[str, Any] = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": search_depth,
            "topic": topic,
            "max_results": max_results,
        }
        if include_domains is not None:
            if not isinstance(include_domains, list) or not all(isinstance(d, str) for d in include_domains):
                raise ValueError(
                    "include_domains must be a list of strings or None.")
            payload["include_domains"] = include_domains
        if exclude_domains is not None:
            if not isinstance(exclude_domains, list) or not all(isinstance(d, str) for d in exclude_domains):
                raise ValueError(
                    "exclude_domains must be a list of strings or None.")
            payload["exclude_domains"] = exclude_domains

        resp = self._session.post(
            self.SEARCH_URL, json=payload, timeout=self._timeout)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, dict):
            raise RuntimeError("Unexpected response from Tavily search API.")
        return data

    def extract(self, url: str) -> Dict[str, Any]:
        if not isinstance(url, str) or not url.strip():
            raise ValueError("url must be a non-empty string.")
        payload = {
            "api_key": self.api_key,
            "url": url,
        }
        resp = self._session.post(
            self.EXTRACT_URL, json=payload, timeout=self._timeout)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, dict):
            raise RuntimeError("Unexpected response from Tavily extract API.")
        return data

    def format_search_results(self, results: Dict[str, Any]) -> str:
        if not isinstance(results, dict):
            return ""
        parts: List[str] = []
        answer = results.get("answer")
        if isinstance(answer, str) and answer.strip():
            parts.append(f"Answer: {answer.strip()}")
        res_list = results.get("results")
        if isinstance(res_list, list):
            for idx, item in enumerate(res_list, start=1):
                if not isinstance(item, dict):
                    continue
                title = item.get("title") or "Untitled"
                url = item.get("url") or ""
                score = item.get("score")
                content = item.get("content") or ""
                snippet = (content[:300] + "...") if isinstance(content,
                                                                str) and len(content) > 300 else content
                line_parts = [f"{idx}. {title}"]
                if isinstance(score, (int, float)):
                    line_parts[-1] += f" (score: {score:.3f})"
                if url:
                    line_parts.append(f"URL: {url}")
                if snippet:
                    line_parts.append(f"Snippet: {snippet}")
                parts.append("\n".join(line_parts))
        if not parts:
            return "No results."
        return "\n\n".join(parts)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        if not isinstance(results, dict):
            return ""
        title = results.get("title") or "Untitled"
        url = results.get("url") or ""
        content = results.get("content") or results.get("text") or ""
        snippet = (content[:1000] + "...") if isinstance(content,
                                                         str) and len(content) > 1000 else content
        parts = [f"Title: {title}"]
        if url:
            parts.append(f"URL: {url}")
        if snippet:
            parts.append(f"Content:\n{snippet}")
        return "\n".join(parts)
