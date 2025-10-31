
import time
import re


class AbstractHtmlConverter:

    def get_text(self, html):
        # Remove script and style elements
        html = re.sub(r'<(script|style).*?>.*?</\1>', '',
                      html, flags=re.DOTALL | re.IGNORECASE)
        # Remove all HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        # Convert HTML entities to their corresponding characters
        text = re.sub(r'&nbsp;', ' ', text)
        text = re.sub(r'&lt;', '<', text)
        text = re.sub(r'&gt;', '>', text)
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'&quot;', '"', text)
        text = re.sub(r'&#39;', "'", text)
        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def benchmark(self, html):
        start = time.perf_counter()
        self.get_text(html)
        end = time.perf_counter()
        return end - start
