
from bs4 import BeautifulSoup
import time
from abc import ABC, abstractmethod


class AbstractHtmlConverter(ABC):

    @abstractmethod
    def get_text(self, html):
        '''
        Returns:
            a text representation of the given HTML snippet.
        '''
        pass

    def benchmark(self, html):
        start_time = time.time()
        self.get_text(html)
        end_time = time.time()
        return end_time - start_time


class HtmlConverter(AbstractHtmlConverter):

    def get_text(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()


# Example usage:
if __name__ == "__main__":
    html_converter = HtmlConverter()
    html = "<html><body>This is a <span>test</span> HTML snippet.</body></html>"
    print(html_converter.get_text(html))
    print(f"Benchmark: {html_converter.benchmark(html)} seconds")
