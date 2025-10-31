class PartitionInfo:
    """
    Class for holding the info of a partition.

    Attributes:
        utt_ids (list): A list of utterance-ids in the partition.
        utt_lengths (list): List with lengths of the utterances (Outermost
                            dimension in the dataset of the container). Since
                            there are maybe multiple containers, every item
                            is a tuple of lengths. They correspond to the
                            length of the utterance in every container, in the
                            order of the containers passed to
                            the ParitioningContainerLoader.
        size (int): The number of bytes the partition will allocate,
                    when loaded.
    """

    def __init__(self):
        self.utt_ids = []
        self.utt_lengths = []
        self.size = 0

    def total_lengths(self):
        """ Return the total length of all utterances for every container. """
        return tuple((sum(x) for x in zip(*self.utt_lengths)))