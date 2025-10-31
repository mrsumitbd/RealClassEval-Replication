
import time
from bs4 import BeautifulSoup
import html2text
import re


class AbstractHtmlConverter:
    '''
    An abstract HTML convert class.
    '''

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


class Html2TextConverter(AbstractHtmlConverter):
    '''
    A concrete HTML convert class using html2text library.
    '''

    def get_text(self, html):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        return h.handle(html)


class BeautifulSoupConverter(AbstractHtmlConverter):
    '''
    A concrete HTML convert class using BeautifulSoup library.
    '''

    def get_text(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()


class SimpleRegexConverter(AbstractHtmlConverter):
    '''
    A concrete HTML convert class using simple regex.
    '''

    def get_text(self, html):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', html)


# Example usage:
if __name__ == "__main__":
    html = "<html><body>This is a <span>test</span> HTML snippet.</body></html>"

    converters = [Html2TextConverter(), BeautifulSoupConverter(),
                  SimpleRegexConverter()]

    for converter in converters:
        time_taken, text = converter.benchmark(html)
        print(f"Converter: {type(converter).__name__}")
        print(f"Time taken: {time_taken} seconds")
        print(f"Text: {text}\n")
