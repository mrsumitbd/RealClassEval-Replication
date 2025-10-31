from future.utils import iteritems

class Record:
    """A record representing a :term:`fastq` formatted record.

    Attributes
    ----------
    identifier : string
       Sequence identifier
    seq : string
       Sequence
    quals : string
       String representation of quality scores.
    format : string
       Quality score format. Can be one of ``sanger``,
       ``phred33``, ``phred64`` or ``solexa``.

    """

    def __init__(self, identifier, seq, quals, entry_format=None):
        self.identifier, self.seq, self.quals, entry_format = (identifier, seq, quals, entry_format)

    def guessFormat(self):
        """return quality score format -
        might return several if ambiguous."""
        c = [ord(x) for x in self.quals]
        mi, ma = (min(c), max(c))
        r = []
        for entry_format, v in iteritems(RANGES):
            m1, m2 = v
            if mi >= m1 and ma < m2:
                r.append(entry_format)
        return r

    def __str__(self):
        return '@%s\n%s\n+\n%s' % (self.identifier, self.seq, self.quals)