class OutputSink:
    '''Abstract output sink for processed markdown text.'''

    def __init__(self):
        self._buffer = []

    def write(self, text: str) -> None:
        self._buffer.append(text)

    def finalize(self) -> None:
        output = ''.join(self._buffer)
        print(output)
