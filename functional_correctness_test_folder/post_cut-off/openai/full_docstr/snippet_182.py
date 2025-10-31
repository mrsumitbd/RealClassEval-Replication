class OutputSink:
    '''Abstract output sink for processed markdown text.'''

    def __init__(self, file_path: str):
        self._file_path = file_path
        self._file = open(file_path, 'w', encoding='utf-8')

    def write(self, text: str) -> None:
        '''Write text to the sink.'''
        self._file.write(text)

    def finalize(self) -> None:
        '''Finalize the output.'''
        self._file.close()
