class Reader:
    """
    Iterate over all maf blocks in a file in order
    """

    def __init__(self, file, **kwargs):
        self.file = file
        self.maf_kwargs = kwargs
        fields = self.file.readline().split()
        if fields[0] != '##maf':
            raise Exception('File does not have MAF header')
        self.attributes = parse_attributes(fields[1:])

    def __next__(self):
        return read_next_maf(self.file, **self.maf_kwargs)

    def __iter__(self):
        return ReaderIter(self)

    def close(self):
        self.file.close()