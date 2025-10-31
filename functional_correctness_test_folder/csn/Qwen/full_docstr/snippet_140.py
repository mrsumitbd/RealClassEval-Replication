
import time
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class AbstractHtmlConverter(ABC):
    '''
    An abstract HTML convert class.
    '''

    @abstractmethod
    def get_text(self, html):
        '''
        Returns:
            a text representation of the given HTML snippet.
        '''
        pass

    def benchmark(self, html):
        '''
        Benchmarks the classes HTML to text converter.
        Returns:
            A tuple of the required time and the obtained text representation.
        '''
        start_time = time.time()
        text = self.get_text(html)
        end_time = time.time()
        return (end_time - start_time, text)


class SimpleHtmlConverter(AbstractHtmlConverter):
    def get_text(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()
