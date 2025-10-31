class OutputSink:
    '''Abstract output sink for processed markdown text.'''

    def write(self, text: str) -> None:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        raise NotImplementedError("Subclasses must implement write().")

    def finalize(self) -> None:
        # Optional hook for cleanup; default is no-op.
        pass
