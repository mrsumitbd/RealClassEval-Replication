class Alignment:

    def __init__(self, sequences):
        self.sequences = sequences

    def fetch(self, reference, start, stop):
        reference_sequence = self.sequences[reference]
        reference_position = 0
        alignment_start = 0
        alignment_stop = 0
        for alignment_position in range(len(reference_sequence)):
            reference_position += reference_sequence[alignment_position] != '-'
            if reference_position == start:
                alignment_start = alignment_position + 1
            if reference_position == stop:
                alignment_stop = alignment_position + 1
        return Alignment({key: value[alignment_start:alignment_stop] for key, value in self.sequences.items()})