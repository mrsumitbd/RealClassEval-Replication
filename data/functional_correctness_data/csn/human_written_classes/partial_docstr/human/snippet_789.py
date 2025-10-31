class Chunk:
    """
    Represents a chunk of data. It is used to pass data between different
    steps of a pipeline.

    Args:
        data (np.ndarray or list): A single array of frames or a list of
                                   separate chunks of frames of equal size.
        offset (int): The index of the first frame in the chunk within
                      the sequence.
        is_last (bool): Whether this is the last chunk of the sequence.
        left_context (int): Number of frames that act as context at the begin
                            of the chunk (left).
        right_context (int): Number of frames that act as context at the end
                             of the chunk (right).
    """

    def __init__(self, data, offset, is_last, left_context=0, right_context=0):
        self.data = data
        self.offset = offset
        self.is_last = is_last
        self.left_context = left_context
        self.right_context = right_context

    def __repr__(self):
        return 'Chunk(data [{}], offset [{}], is-last [{}], left[{}], right[{}])'.format(self.data.shape, self.offset, self.is_last, self.left_context, self.right_context)