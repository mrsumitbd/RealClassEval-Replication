class SubCommand:
    """
    a subcommand for jupytext-config
    """

    def __init__(self, name, help):
        self.name = name
        self.help = help

    def main(self, args):
        """
        return 0 if all goes well
        """
        raise NotImplementedError()