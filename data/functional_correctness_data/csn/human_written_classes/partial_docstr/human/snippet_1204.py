class Group:
    """ Represent a part of a compound formula

    :param group: iterable of Group/Element parts
    :param multiplier: multiplier in subscript or prefix of group
    :param dotted: True of the group is like '.2H2O'

    """

    def __init__(self, group, multiplier=1, dotted=False):
        self.group = group
        self.multiplier = multiplier
        self.dotted = dotted

    def count(self):
        return count_with_multiplier(self.group, self.multiplier)

    def __repr__(self):
        return 'Group({}, multiplier={}, dotted={})'.format(self.group, self.multiplier, self.dotted)