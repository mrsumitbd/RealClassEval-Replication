
from typing import List, Dict, Any
import random


class TavilySearchService:

    def __init__(self):
        self._dummy_db = [
            {
                "title": "Python Programming Language",
                "url": "https://www.python.org/",
                "snippet": "Python is a programming language that lets you work quickly and integrate systems more effectively.",
                "domain": "python.org"
            },
            {
                "title": "Learn Python - Free Interactive Python Tutorial",
                "url": "https://www.learnpython.org/",
                "snippet": "LearnPython.org is a free interactive Python tutorial for people who want to learn Python, fast.",
                "domain": "learnpython.org"
            },
            {
                "title": "Real Python: Python Tutorials",
                "url": "https://realpython.com/",
                "snippet": "Learn Python online with tutorials, courses, and books from Real Python.",
                "domain": "realpython.com"
            },
            {
                "title": "Wikipedia: Python (programming language)",
                "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
                "snippet": "Python is an interpreted high-level general-purpose programming language.",
                "domain": "wikipedia.org"
            },
            {
                "title": "W3Schools Python Tutorial",
                "url": "https://www.w3schools.com/python/",
                "snippet": "Python is a popular programming language. Learn more about Python at W3Schools.",
                "domain": "w3schools.com"
            }
        ]

    def search(self, query: str, search_depth: str = 'basic', topic: str = 'general', include_domains: List[str] | None = None, exclude_domains: List[str] | None = None, max_results: int = 5) -> Dict[str, Any]:
        results = []
        for item in self._dummy_db:
            if include_domains and item["domain"] not in include_domains:
                continue
            if exclude_domains and item["domain"] in exclude_domains:
                continue
            if query.lower() in item["title"].lower() or query.lower() in item["snippet"].lower():
                results.append(item)
        if not results:
            # fallback: return random results if nothing matches
            results = random.sample(self._dummy_db, min(
                max_results, len(self._dummy_db)))
        else:
            results = results[:max_results]
        return {
            "query": query,
            "search_depth": search_depth,
            "topic": topic,
            "results": results
        }

    def extract(self, url: str) -> Dict[str, Any]:
        for item in self._dummy_db:
            if item["url"] == url:
                return {
                    "url": url,
                    "title": item["title"],
                    "content": item["snippet"],
                    "domain": item["domain"]
                }
        return {
            "url": url,
            "title": "Unknown",
            "content": "No content found for the given URL.",
            "domain": ""
        }

    def format_search_results(self, results: Dict[str, Any]) -> str:
        output = [f"Search Results for '{results.get('query', '')}':"]
        for idx, item in enumerate(results.get("results", []), 1):
            output.append(
                f"{idx}. {item['title']}\n   URL: {item['url']}\n   Snippet: {item['snippet']}")
        return "\n".join(output)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        return (
            f"Extracted Content from {results.get('url', '')}:\n"
            f"Title: {results.get('title', '')}\n"
            f"Domain: {results.get('domain', '')}\n"
            f"Content: {results.get('content', '')}"
        )
