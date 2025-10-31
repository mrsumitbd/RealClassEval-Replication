class Command:
    """base class for commands"""
    repeatable = False

    def __init__(self):
        self.prehook = None
        self.posthook = None
        self.undoable = False
        self.help = self.__doc__

    def apply(self, ui):
        """code that gets executed when this command is applied"""
        pass