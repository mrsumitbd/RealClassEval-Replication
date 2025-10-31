class _NullSequence:
    """Contains the terminal character sequence for the typed null suffix of the given IonType, starting with the first
    character after the one which disambiguated the type.

    For example, SYMBOL's _NullSequence contains the characters 'mbol' because 'null.s' is ambiguous until 'y' is found,
    at which point it must end in 'mbol'.

    Instances are used as leaves of the typed null prefix tree below.
    """

    def __init__(self, ion_type, sequence):
        self.ion_type = ion_type
        self.sequence = sequence

    def __getitem__(self, item):
        return self.sequence[item]