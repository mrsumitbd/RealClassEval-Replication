class InstanceVarXWithInt:
    """Class with an instance var x and an __int__ method"""

    def __init__(self):
        self.x = 42

    def __int__(self):
        return 42