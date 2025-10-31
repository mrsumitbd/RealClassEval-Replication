class FileReader:
    """Class for reading a file without "OSError: Too many open files".
        If keep_file_open==True, data are read in small batches and files are being reopened
        and closed for each reading. Last position in file is kept.

        Args:
                fn (str): File name of the file to be read.
                keep_file_open (bool): Keep the file open.
                buffer_lines (int): Number of lines read as a single batch.
        """

    def __init__(self, fn, keep_file_open=False, buffer_lines=50):
        self.fn = fn
        self.keep_file_open = keep_file_open
        if self.keep_file_open:
            self.fo = open(fn)
        else:
            self.fo = None
            self.buffer = []
            self.buffer_lines = buffer_lines
            self._closed = False
            self.file_pos = 0

    def readline(self):
        if self.keep_file_open:
            return self.fo.readline()
        else:
            if len(self.buffer) == 0:
                self.fo = open(self.fn)
                self.fo.seek(self.file_pos)
                for _ in range(self.buffer_lines):
                    line = self.fo.readline()
                    self.buffer.append(line)
                self.file_pos = self.fo.tell()
                self.fo.close()
            return self.buffer.pop(0)

    def close(self):
        if self.keep_file_open:
            self.fo.close()
        else:
            self._closed = True

    @property
    def closed(self):
        if self.keep_file_open:
            return self.fo.closed
        else:
            return self._closed