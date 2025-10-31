
class AbstractHtmlConverter:

    def get_text(self, html):
        raise NotImplementedError("Subclasses must implement this method")

    def benchmark(self, html):
        import time
        start_time = time.time()
        result = self.get_text(html)
        end_time = time.time()
        return result, end_time - start_time
