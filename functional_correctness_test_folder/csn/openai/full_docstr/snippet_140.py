
import time
from html.parser import HTMLParser


class AbstractHtmlConverter:
    """
    An abstract HTML convert class.
    """

    def get_text(self, html):
        """
        Returns:
            a text representation of the given HTML snippet.
        """
        class _TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text_parts = []

            def handle_data(self, data):
                self.text_parts.append(data)

            def get_text(self):
                return "".join(self.text_parts)

        extractor = _TextExtractor()
        extractor.feed(html)
        return extractor.get_text()

    def benchmark(self, html):
        """
        Benchmarks the class's HTML to text converter.
        Returns:
            A tuple of the required time (in seconds) and the obtained text representation.
        """
        start = time.perf_counter()
        text = self.get_text(html)
        elapsed = time.perf_counter() - start
        return elapsed, text
