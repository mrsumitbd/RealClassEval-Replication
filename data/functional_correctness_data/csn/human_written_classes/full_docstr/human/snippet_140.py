from time import time

class AbstractHtmlConverter:
    """
    An abstract HTML convert class.
    """

    def get_text(self, html):
        """
        Returns:
            a text representation of the given HTML snippet.
        """
        raise NotImplementedError

    def benchmark(self, html):
        """
        Benchmarks the classes HTML to text converter.

        Returns:
            A tuple of the required time and the obtained text representation.
        """
        start_time = time()
        for _ in range(TRIES):
            text = self.get_text(html)
        return (time() - start_time, text)