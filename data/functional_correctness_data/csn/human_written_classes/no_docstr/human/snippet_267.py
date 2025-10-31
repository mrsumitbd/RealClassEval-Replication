class FieldEmbeddings:

    def __init__(self):
        self._n_vocab = None

    @property
    def n_vocab(self) -> int:
        return self._n_vocab

    @n_vocab.setter
    def n_vocab(self, val):
        self._n_vocab = val

    def __repr__(self):
        s = f'{self.__class__.__name__}(n_vocab={self._n_vocab})'
        return s