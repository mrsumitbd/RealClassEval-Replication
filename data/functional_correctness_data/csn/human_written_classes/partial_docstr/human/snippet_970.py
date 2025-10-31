class Settings:
    """Command-line arguments that are set programmatically instead of by
    parsing the command line. For example:

        args = Settings(
            server='http://localhost:5000',
            no_browser=True,
            backup=True,
            timeout=60,
        )
        assignment = Assignment(args)
    """

    def __init__(self, **kwargs):
        from client.cli.ok import parse_input
        self.args = parse_input([])
        self.update(**kwargs)

    def __getattr__(self, attr):
        return getattr(self.args, attr)

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self.args, k, v)

    def __repr__(self):
        cls = type(self).__name__
        return '{0}({1})'.format(cls, vars(self.args))