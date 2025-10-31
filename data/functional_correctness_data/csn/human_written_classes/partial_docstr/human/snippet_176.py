class Macro:
    """Class to encapsulate undefined macro references"""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Macro("{self.name}")'

    def __eq__(self, other):
        return self.name == other.name