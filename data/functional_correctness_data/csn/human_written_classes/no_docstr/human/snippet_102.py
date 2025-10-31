class Vocab:

    def __init__(self, w2i):
        self.w2i = dict(w2i)
        self.i2w = {i: w for w, i in w2i.items()}

    @classmethod
    def from_corpus(cls, corpus):
        w2i = {}
        for sent in corpus:
            for word in sent:
                w2i.setdefault(word, len(w2i))
        return Vocab(w2i)

    def size(self):
        return len(self.w2i.keys())