
import re
import time
from html import unescape


class AbstractHtmlConverter:
    """
    A simple HTML to plain‑text converter with a benchmark helper.
    """

    _TAG_RE = re.compile(r'<[^>]+>')

    def get_text(self, html: str) -> str:
        """
        Convert an HTML string to plain text by removing tags and unescaping entities.
        """
        if not isinstance(html, str):
            raise TypeError("html must be a string")
        # Remove tags
        text = self._TAG_RE.sub('', html)
        # Unescape HTML entities
        text = unescape(text)
        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def benchmark(self, html: str, iterations: int = 1000) -> float:
        """
        Measure the average time (in seconds) taken by get_text over a number of iterations.
        """
        if not isinstance(iterations, int) or iterations <= 0:
            raise ValueError("iterations must be a positive integer")
        start = time.perf_counter()
        for _ in range(iterations):
            self.get_text(html)
        end = time.perf_counter()
        return (end - start) / iterations
