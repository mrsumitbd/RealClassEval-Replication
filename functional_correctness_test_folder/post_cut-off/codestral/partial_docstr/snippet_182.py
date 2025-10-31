
class OutputSink:
    '''Abstract output sink for processed markdown text.'''

    def write(self, text: str) -> None:
        pass

    def finalize(self) -> None:
        pass
