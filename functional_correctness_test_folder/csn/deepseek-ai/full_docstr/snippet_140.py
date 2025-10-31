
import time


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
        elapsed_time = end_time - start_time
        return (elapsed_time, text)
