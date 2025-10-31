class Term:
    """
    Base class for the terms of a TDL conjunction.

    All terms are defined to handle the binary '&' operator, which
    puts both into a Conjunction:

    >>> TypeIdentifier('a') & TypeIdentifier('b')
    <Conjunction object at 140008950372168>

    Args:
        docstring (str): documentation string

    Attributes:
        docstring (str): documentation string
    """

    def __init__(self, docstring=None):
        self.docstring = docstring

    def __repr__(self):
        return '<{} object at {}>'.format(type(self).__name__, id(self))

    def __and__(self, other):
        if isinstance(other, Term):
            return Conjunction([self, other])
        elif isinstance(other, Conjunction):
            return Conjunction([self] + other._terms)
        else:
            return NotImplemented