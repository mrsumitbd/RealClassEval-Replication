
import re
import time


class AbstractHtmlConverter:

    def get_text(self, html):
        '''
        Returns:
            a text representation of the given HTML snippet.
        '''
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def benchmark(self, html):
        start_time = time.time()
        self.get_text(html)
        end_time = time.time()
        return end_time - start_time
