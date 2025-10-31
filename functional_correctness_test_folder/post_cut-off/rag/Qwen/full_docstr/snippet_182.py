
class OutputSink:
    '''Abstract output sink for processed markdown text.'''

    def write(self, text: str) -> None:
        '''Write text to the sink.'''
        raise NotImplementedError(
            "This method should be overridden by subclasses")

    def finalize(self) -> None:
        '''Finalize the output.'''
        raise NotImplementedError(
            "This method should be overridden by subclasses")
