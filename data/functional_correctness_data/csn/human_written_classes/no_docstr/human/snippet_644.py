class FastaWriter:

    def __init__(self, file, columns=50):
        self.file = file
        self.columns = columns

    def write(self, seq):
        print(f'>{seq.name}', file=self.file)
        text = seq.text
        if self.columns is not None and self.columns > 0:
            text = '\n'.join((text[ix:ix + self.columns] for ix in range(0, len(text), self.columns)))
        print(text, file=self.file)

    def close(self):
        assert self.file is not None
        self.file.close()
        self.file = None