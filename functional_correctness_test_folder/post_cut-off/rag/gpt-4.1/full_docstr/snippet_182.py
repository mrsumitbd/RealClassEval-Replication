class OutputSink:
    '''Abstract output sink for processed markdown text.'''

    def write(self, text: str) -> None:
        '''Write text to the sink.'''
        raise NotImplementedError("Subclasses must implement write()")

    def finalize(self) -> None:
        '''Finalize the output.'''
        pass
