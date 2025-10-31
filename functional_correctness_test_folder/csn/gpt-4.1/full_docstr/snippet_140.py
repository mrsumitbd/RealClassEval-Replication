
import time
import re
from html import unescape


class AbstractHtmlConverter:
    '''
    An abstract HTML convert class.
    '''

    def get_text(self, html):
        '''
        Returns:
            a text representation of the given HTML snippet.
        '''
        # Remove script and style elements
        html = re.sub(r'<(script|style).*?>.*?</\1>', '',
                      html, flags=re.DOTALL | re.IGNORECASE)
        # Remove all HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        # Unescape HTML entities
        text = unescape(text)
        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def benchmark(self, html):
        '''
        Benchmarks the classes HTML to text converter.
        Returns:
            A tuple of the required time and the obtained text representation.
        '''
        start = time.perf_counter()
        text = self.get_text(html)
        end = time.perf_counter()
        return (end - start, text)
