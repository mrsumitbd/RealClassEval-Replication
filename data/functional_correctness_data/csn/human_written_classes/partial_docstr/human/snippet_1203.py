class Compound:
    """ Represents a full compound formula

    :param group: iterable of Group/Element
    :param dottedgroup: A Group if there is a .H2O part, None otherwise
    :param phase: The phase if there is a [phase] part, None otherwise

    """

    def __init__(self, group, dottedgroup=None, phase=None):
        self.group = [group]
        if dottedgroup:
            self.group.append(dottedgroup)
        self.phase = phase

    def count(self):
        return count_with_multiplier(self.group, multiplier=1)

    def molar_mass(self):
        return sum((_element_dictionary_[element].molar_mass * count for element, count in self.count().items()))

    def __repr__(self):
        return 'Compound({}, {})'.format(self.group, self.phase)