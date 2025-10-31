class Phrase:
    """
    represents one extracted phrase
    """

    def __init__(self, text, rank, count, phrase_list):
        self.text = text
        self.rank = rank
        self.count = count
        self.chunks = [p.chunk for p in phrase_list]

    def __repr__(self):
        return self.text