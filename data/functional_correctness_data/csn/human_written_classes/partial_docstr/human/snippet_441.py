class registerCommand:
    """
    Decorator used to register a :class:`Command` as
    handler for command `name` in `mode` so that it
    can be looked up later using :func:`lookup_command`.

    Consider this example that shows how a :class:`Command` class
    definition is decorated to register it as handler for
    'save' in mode 'thread' and add boolean and string arguments::

    .. code-block::

        @registerCommand('thread', 'save', arguments=[
            (['--all'], {'action': 'store_true', 'help':'save all'}),
            (['path'], {'nargs':'?', 'help':'path to save to'})],
            help='save attachment(s)')
        class SaveAttachmentCommand(Command):
            pass

    """

    def __init__(self, mode, name, help=None, usage=None, forced=None, arguments=None):
        """
        :param mode: mode identifier
        :type mode: str
        :param name: command name to register as
        :type name: str
        :param help: help string summarizing what this command does
        :type help: str
        :param usage: overides the auto generated usage string
        :type usage: str
        :param forced: keyword parameter used for commands constructor
        :type forced: dict (str->str)
        :param arguments: list of arguments given as pairs (args, kwargs)
                          accepted by
                          :meth:`argparse.ArgumentParser.add_argument`.
        :type arguments: list of (list of str, dict (str->str)
        """
        self.mode = mode
        self.name = name
        self.help = help
        self.usage = usage
        self.forced = forced or {}
        self.arguments = arguments or []

    def __call__(self, klass):
        helpstring = self.help or klass.__doc__
        argparser = CommandArgumentParser(description=helpstring, usage=self.usage, prog=self.name, add_help=False)
        for args, kwargs in self.arguments:
            argparser.add_argument(*args, **kwargs)
        COMMANDS[self.mode][self.name] = (klass, argparser, self.forced)
        return klass