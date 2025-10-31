class Reader:
    """Iterate over all axt blocks in a file in order"""

    def __init__(self, file, species1=None, species2=None, species_to_lengths=None, support_ids=False):
        self.file = file
        self.species1 = species1
        if self.species1 is None:
            self.species1 = 'species1'
        self.species2 = species2
        if self.species2 is None:
            self.species2 = 'species2'
        self.species_to_lengths = species_to_lengths
        self.support_ids = support_ids
        self.attributes = {}

    def __next__(self):
        return read_next_axt(self.file, self.species1, self.species2, self.species_to_lengths, self.support_ids)

    def __iter__(self):
        return ReaderIter(self)

    def close(self):
        self.file.close()