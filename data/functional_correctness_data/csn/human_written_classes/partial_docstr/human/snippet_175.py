class Command:
    """Base class for commands"""

    def __init__(self, verb, verbProg):
        self.verb = verb
        self.verbProg = verbProg

    @staticmethod
    def help_description():
        return ''

    def _do_command(self, player):
        pass

    def __call__(self, player):
        print(self.verbProg.capitalize() + '...')
        self._do_command(player)