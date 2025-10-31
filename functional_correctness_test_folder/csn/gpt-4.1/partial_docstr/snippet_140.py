
import time
from html.parser import HTMLParser


class AbstractHtmlConverter:
    class _TextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text_parts = []

        def handle_data(self, data):
            self.text_parts.append(data)

        def get_text(self):
            return ''.join(self.text_parts)

    def get_text(self, html):
        '''
        Returns:
            a text representation of the given HTML snippet.
        '''
        parser = self._TextExtractor()
        parser.feed(html)
        return parser.get_text()

    def benchmark(self, html):
        start = time.perf_counter()
        self.get_text(html)
        end = time.perf_counter()
        return end - start
