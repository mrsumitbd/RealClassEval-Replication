import attr

@attr.s(slots=True, repr=False)
class HGVSPosition:
    """
    HGVSPosition -- Represent partial HGVS tags that refer to a position without alleles

    :param str ac: sequence accession
    :param str type: type of sequence and coordinate
    :param str pos: sequence position
    :param str gene: gene symbol (may be None)

    """
    ac = attr.ib()
    type = attr.ib()
    pos = attr.ib()
    gene = attr.ib(default=None)

    def __str__(self):
        g = '' if not self.gene else '(' + self.gene + ')'
        return '{self.ac}{g}:{self.type}.{self.pos}'.format(self=self, g=g)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, ', '.join((a.name + '=' + str(getattr(self, a.name)) for a in self.__attrs_attrs__)))