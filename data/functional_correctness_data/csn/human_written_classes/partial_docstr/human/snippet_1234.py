class SwitchOnValue:
    """
    don't need to wait result
    """

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'SwitchOnValue({})'.format(self.value)