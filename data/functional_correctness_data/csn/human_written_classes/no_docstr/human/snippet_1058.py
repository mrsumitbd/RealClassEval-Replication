class SequenceSet:

    def __init__(self, sequences):
        self._sequences = sequences

    def fetch(self, chromosome, start, stop):
        return self._sequences[chromosome][start:stop]