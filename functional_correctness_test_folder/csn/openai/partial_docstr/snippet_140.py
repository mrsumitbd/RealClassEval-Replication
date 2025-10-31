
import time
from html.parser import HTMLParser


class AbstractHtmlConverter:
    """
    A simple HTML to text converter with benchmarking support.
    """

    class _TextExtractor(HTMLParser):
        """
        Internal HTML parser that collects text data.
        """

        def __init__(self):
            super().__init__()
            self._parts = []

        def handle_data(self, data):
            self._parts.append(data)

        def get_text(self):
            return ''.join(self._parts)

    def get_text(self, html):
        """
        Convert an HTML snippet into plain text.

        Parameters
        ----------
        html : str
            The HTML snippet to convert.

        Returns
        -------
        str
            The extracted text.
        """
        parser = self._TextExtractor()
        parser.feed(html)
        parser.close()
        return parser.get_text()

    def benchmark(self, html):
        """
        Measure the time taken to convert the given HTML snippet to text.

        Parameters
        ----------
        html : str
            The HTML snippet to convert.

        Returns
        -------
        dict
            A dictionary containing:
                - 'text': the extracted text,
                - 'elapsed': time in seconds taken for conversion.
        """
        start = time.perf_counter()
        text = self.get_text(html)
        elapsed = time.perf_counter() - start
        return {'text': text, 'elapsed': elapsed}
