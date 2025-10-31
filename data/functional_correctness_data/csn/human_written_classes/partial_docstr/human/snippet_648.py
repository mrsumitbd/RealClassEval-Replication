class CIGARElement:
    """represents elements of a CIGAR string and provides methods for
    determining the number of ref and tgt bases consumed by the
    operation"""
    __slots__ = ('len', 'op')

    def __init__(self, len, op):
        self.len = len
        self.op = op

    @property
    def ref_len(self):
        """returns number of nt/aa consumed in reference sequence for this edit"""
        return self.len if self.op in '=INX' else 0

    @property
    def tgt_len(self):
        """returns number of nt/aa consumed in target sequence for this edit"""
        return self.len if self.op in '=DX' else 0