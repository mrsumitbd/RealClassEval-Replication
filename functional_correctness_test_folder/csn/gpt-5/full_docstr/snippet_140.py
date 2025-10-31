class AbstractHtmlConverter:
    '''
    An abstract HTML convert class.
    '''

    def get_text(self, html):
        '''
        Returns:
            a text representation of the given HTML snippet.
        '''
        raise NotImplementedError("Subclasses must implement get_text")

    def benchmark(self, html):
        '''
        Benchmarks the classes HTML to text converter.
        Returns:
            A tuple of the required time and the obtained text representation.
        '''
        import time
        start = time.perf_counter()
        text = self.get_text(html)
        end = time.perf_counter()
        return (end - start, text)
