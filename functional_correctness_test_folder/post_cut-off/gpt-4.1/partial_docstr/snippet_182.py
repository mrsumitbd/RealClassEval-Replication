
class OutputSink:
    '''Abstract output sink for processed markdown text.'''

    def write(self, text: str) -> None:
        raise NotImplementedError("Subclasses must implement write()")

    def finalize(self) -> None:
        raise NotImplementedError("Subclasses must implement finalize()")
