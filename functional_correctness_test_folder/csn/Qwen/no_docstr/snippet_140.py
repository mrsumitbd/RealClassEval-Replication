
class AbstractHtmlConverter:

    def get_text(self, html):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()

    def benchmark(self, html):
        import time
        start_time = time.time()
        self.get_text(html)
        end_time = time.time()
        return end_time - start_time
