
class OutputSink:
    '''Abstract output sink for processed markdown text.'''

    def write(self, text: str) -> None:
        raise NotImplementedError("Subclasses should implement this method.")

    def finalize(self) -> None:
        raise NotImplementedError("Subclasses should implement this method.")
