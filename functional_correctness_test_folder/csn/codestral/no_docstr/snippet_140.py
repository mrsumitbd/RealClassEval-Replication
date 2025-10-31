
class AbstractHtmlConverter:

    def get_text(self, html):

        raise NotImplementedError("Subclasses must implement this method")

    def benchmark(self, html):

        raise NotImplementedError("Subclasses must implement this method")
