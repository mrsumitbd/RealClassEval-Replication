
class OutputSink:
    '''Abstract output sink for processed markdown text.'''

    def __init__(self, file_path: str | None = None, file_obj=None):
        """
        Create an output sink.

        Parameters
        ----------
        file_path : str, optional
            Path to a file to write to. If ``file_obj`` is provided, this
            argument is ignored.
        file_obj : file-like, optional
            An already opened file-like object. If provided, the sink will
            write to this object and will not close it on ``finalize``.
        """
        if file_obj is not None:
            self._file = file_obj
            self._own_file = False
        else:
            if file_path is None:
                raise ValueError(
                    "Either file_path or file_obj must be provided")
            self._file = open(file_path, "w", encoding="utf-8")
            self._own_file = True

    def write(self, text: str) -> None:
        '''Write text to the sink.'''
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        self._file.write(text)

    def finalize(self) -> None:
        '''Finalize the output.'''
        if self._own_file:
            self._file.close()
